# Optional

`null`은 값이 없음을 나타내는 참조이다. 자바에서 `null` 참조를 사용하면 다음과 같은 문제들이 발생한다.

- `null` 참조에 접근하여 사용하려고 하면 `NullPointerException` 예외가 발생한다. 자바에서 가장 흔히 발생하는 예외이다.
- `NullPointerException` 예외가 발생하지 않도록 인스턴스가 `null`인지 확인하는 코드를 추가해야 한다. 때문에 `return` 출구가 여러개 생기거나 중첩된 `null` 확인 코드가 생겨 가독성이 떨어지게 된다.
- `null`은 아무 의미도 표현하지 않기 때문에 값이 없음을 표현하기에는 적절하지 않다. `null`을 남발하면 어떤 의미로 사용되었는지 알 수 없다.

Java 8은 이러한 `null` 관련 문제들을 해결하기 위해 `java.util.Optional<T>`라는 클래스를 제공한다. `Optional`은 값을 감싸서 `null` 참조로부터 발생하는 문제들을 마주하지 않게 도와준다. 

`Optional`을 이용하면 값이 없는 상황이 데이터의 문제인지 알고리즘의 버그인지 명확히 구분할 수 있다. 하지만 모든 `null` 참조를 `Optional`로 대치하는 것은 바람직하지 않다. 반드시 값이 필요한 곳에서 `Optional`을 사용하게 되면 오히려 고쳐야할 문제를 감추는 꼴이 되어버린다. 따라서 이를 감싸지 않고 명확하게 드러내는 것이 더 좋은 방법이다. `Optional`의 역할은 더 이해하기 쉬운 API를 설계하도록 돕는 것이다.

## Optional 사용 방법
`Optional`은 선택형값을 캡슐화하는 클래스이다. `Optional`로 값을 감싸서 값이 없을 수 있음을 표현할 수 있다. `Optional` 객체에 값이 존재하는지 판단할 수 있고, 값을 꺼내어 사용할 수도 있다. `Optional`의 값이 없다면 기본값을 지정할 수도 있고, 특정 예외를 발생시킬 수도 있다.

### Optional 객체 생성
`Optional` 객체는 아래와 같이 다양한 방법으로 만들 수 있다.

```java
Member member = new Member("member1", 10);

// Optional.of는 null이 아닌 값을 포함하는 Optional 객체를 만든다.
Optional<Member> optMember1 = Optional.of(member);
// 인수로 받은 값이 null 이라면 NullPointerException이 발생한다.
Optional<Member> optMember3 = Optional.of(null);

// Optional.ofNullable은 null을 담을 수 있는 Optional 객체를 만든다.
Optional<Member> optMember2 = Optional.ofNullable(member);
// 인수로 null이 넘어와도 예외를 발생시키지 않고 빈 Optional 객체를 반환한다.
Optional<Member> optMember4 = Optional.ofNullable(null);

// 빈 Optional 객체를 반환한다. 
// Optional.ofNullable에서 값으로 null이 넘어오면 
// 내부에서 Optional.empty()를 호출하여 빈 Optional을 반환한다.
Optional<Member> empty = Optional.empty();
```

### Optional 값 존재 유무 확인
`Optional` 객체의 `isPresent` 메서드와 `isEmpty` 메서드를 사용하면 해당 `Optional`이 값을 가지는지 아닌지 확인할 수 있다. 해당 메서드들은 `boolean`을 반환한다.

```java
Optional<Member> optMember1 = Optional.ofNullable(new Member("member1", 10));
Optional<Member> optMember2 = Optional.empty();

// true
boolean optMember1IsPresent = optMember1.isPresent();
// false
boolean optMember1IsEmpty = optMember1.isEmpty();

// false
boolean optMember2IsPresent = optMember2.isPresent();
// true
boolean optMember2IsEmpty = optMember2.isEmpty();
```

### Optional 값 사용
값을 감싸는 `Optional`을 제거하고 해당 값을 꺼낼 수 있다. `get`, `orElse`, `orElseGet`, `orElseThrow` 메서드를 제공한다.
또한 `Optional`에 값이 존재하면 특정 동작을 실행하게 하는 `ifPresent`, `ifPresentorElse` 메서드를 제공한다.

#### get 메서드
`get()` 메서드는 값을 읽는 가장 간단한 메서드이면서 가장 안전하지 않은 메서드이다. 값이 있으면 해당 값을 반환하고, 값이 없으면 `NoSuchElementException` 예외를 발생시킨다. 때문에 `Optional`에 값이 있다고 확인할 수 있는 상황을 제외하면 `get()` 메서드를 사용하지 않는 것이 바람직하다.

```java
Optional<Member> optMember1 = Optional.ofNullable(new Member("member1", 10));
// Optional<Member>에서 값이 있다면 Member 객체를 꺼낸다.
Member member = optMember1.get();

Optional<Member> empty = Optional.empty();
// 값이 없기 때문에 NoSuchElementException 예외가 발생한다.
Member memberEmtpy = empty.get();

/* *** 안티 패턴 예 *** */
Member antiMember = null;
if (optMember1.isPresent()) {
    antiMember = optMember1.get();
}
// 가능하다면 아래 메서드들을 사용하자.
```

#### orElse, orElseGet, orElseThrow 메서드
`orElse(T other)` 메서드는 `Optional`에 값이 있다면 해당 값을 반환하고, 값이 없으면 인자로 받은 `other` 객체를 반환한다.

```java
Optional<Member> optMember = Optional.ofNullable(new Member("member1", 10));
// Optional<Member>에서 값이 있다면 Member 객체를 꺼낸다.
// Optional<Member>에 값이 없다면 인자로 받은 기본값을 반환한다.
Member member = optMember.orElse(new Member("default", 0));
// 여기서는 값이 있기 때문에 Member : {"member1", 10} 이 반환된다.
```

`orElseGet(Supplier<? extends T> supplier)` 메서드는 `orElse` 메서드와 같은 기능을 한다. 다만 `orElse`는 이미 생성된 값을 반환하는 반면, `orElseGet` 메서드는 `Supplier` 함수형 인터페이스를 인자로 받아서 값이 없을 때에만 이를 실행하여 기본값을 생성한다.

```java
Optional<Member> optMember = Optional.ofNullable(null);
// Optional<Member>에서 값이 있다면 Member 객체를 꺼낸다.
// Optional<Member>에 값이 없다면 인자로 받은 Supplier를 실행하여 결과를 반환한다.
Member member = optMember.orElseGet(
        () -> new Member("default", 0));
// 여기서는 값이 null로 없기 때문에 Supplier를 실행하여 반환받은
// Member : {"default", 0} 이 반환된다.
```

`orElseThrow(Supplier<? extends X> exceptionSupplier)` 메서드는 `Optional`에 값이 있다면 해당 값을 반환하고, 값이 없으면 인자로 받은 `Supplier` 함수형 인터페이스를 실행하여 예외를 발생시킨다. 값이 없을 때 기본값을 반환하지 않고 지정한 예외를 발생시킬 수 있다는 점에서 `get`, `orElseGet` 메서드와 차이를 보인다. `orElseThrow` 메서드는 `Supplier` 인자를 지정하지 않을 수 있다. 이를 지정하지 않으면 `Optional`에 값이 없을 때 `NoSuchElementException`을 발생시킨다.

```java
Optional<Member> optMember = Optional.ofNullable(null);
// Optional<Member>에서 값이 있다면 Member 객체를 꺼낸다.
// Optional<Member>에 값이 없다면 인자로 받은 Supplier를 실행한 예외를 발생시킨다.
Member member = optMember.orElseThrow(
        () -> throw new CustomException("커스텀 예외 발생"));
// 여기서는 값이 null로 없기 때문에 Supplier를 실행한 결과인
// CustomException 예외가 발생한다.

// orElseThrow 메서드에 Supplier 함수형 인터페이스 인자를 넘기지 않으면
// NoSuchElementException 예외가 발생한다.
Member member2 = optMember.orElseThrow();
```

#### ifPresent, ifPresentorElse 메서드

#### or 메서드

#### filter, map, flatMap 메서드

