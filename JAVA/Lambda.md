# Lambda
## 람다 사용 방법
람다 표현식은 익명 클래스처럼 이름이 없는 함수이면서 메서드를 인수로 전달할 수 있다. 람다 표현식은 메서드와 달리 특정 클래스에 종속되지 않기 때문에 함수라고 부른다.

람다 표현식은 파라미터, 화살표, 바디로 구성된다.

```java
// 화살표 -> 는 람다의 파라미터 리스트와 바디를 구분한다. 화살표 좌측이 파라미터 리스트, 우측이 바디이다.
(Integer i1, Integer i2) -> i1.compareTo(i2);
```

람다의 표현 방식은 표현식 스타일과 블록 스타일의 두가지로 볼 수 있다. 
표현식 스타일에서는 `return`을 사용하지 않는다. 해당 표현식의 값을 람다의 반환값으로 사용한다. 해당 표현식의 결과가 `void`이면 람다의 반환 타입은 `void`가 된다. 
블록 스타일을 사용하면 `return`을 통해 반환값을 지정해준다. `return`을 통한 반환값을 지정해주지 않으면 람다의 반환 타입은 `void`가 된다.

```java
// 표현식 스타일
(params) -> expression

// 블록 스타일
(params) -> { statements; }
```

람다 표현식은 함수형 인터페이스의 추상 메서드 구현을 직접 전달할 수 있다. 따라서 람다의 전체 표현식을 함수형 인터페이스의 인스턴스로 취급할 수 있다. 함수형 인터페이스는 `Comparator`, `Runnable` 등과 같이 오직 하나의 추상 메서드만을 지정하는 인터페이스이다.

```java
// Runnable은 run() 하나만을 추상 메서드로 갖는 함수형 인터페이스이다.
// @FunctionalInterface 은 함수형 인터페이스임을 가리키는 애노테이션.
// 해당 애노테이션이 붙어있는데 함수형 인터페이스가 아니라면(추상메서드가 하나가 아니라면) 컴파일 에러가 발생.
@FunctionalInterface 
public interface Runnable {
    public abstract void run();
}

public static void process(Runnable r) {
	r.run();
}

// 익명 클래스를 이용하여 Runnable을 구현한 객체를 전달한다.
process(new Runnable() {
	@Override
	public void run() {
		System.out.println("Hello World!");
	}
});

// 람다를 이용하여 Runnable의 run()을 구현한 인스턴스를 전달한다.
process(() -> System.out.println("Hello World!!"));
```

- 함수형 인터페이스 : 오직 하나의 추상 메서드만 지정하는 인터페이스. ex) Comparator, Runnable 등
- java.util.function 패키지를 통해 여러 함수형 인터페이스를 제공한다. `Predicate`, `Consumer`, `Function` 등이 대표적
	- `java.util.function.Predicate<T>` 인터페이스는 `boolean test(T t)`를 제공한다. T 형식의 객체를 사용하는 불리언 표현식이 필요한 상황에서 이를 사용할 수 있다.
	- `java.util.function.Consumer<T>` 인터페이스는 `void accept(T t)`를 제공한다. T 형식의 객체를 인수로 받아 어떠한 동작을 수행하고 싶을 때 이를 사용할 수 있다.
	- `java.util.function.Function<T, R>` 인터페이스는 `R apply(T t)`를 제공한다. T 형식의 객체를 인수로 받아 R 객체를 반환하는, 입력을 출력으로 매핑하는 경우 이를 사용할 수 있다.


## 람다 형식 검사, 추론
자바 컴파일러는 람다 표현식이 사용된 콘텍스트를 이용하여 람다 표현식과 관련된 함수형 인터페이스를 추론한다.

```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);
}

public <T, R> List<R> map(List<T> list, Function<T, R> f) {
	List<R> result = new ArrayList<>();
	for (T t : list) {
		result.add(f.apply(t));
	}
	return result;
}

// 람다가 사용되는 컨텐스트를 통해 람다의 형식을 추론할 수 있다.
// 여기서는 map() 메서드의 Function f 파라미터 자리에 람다가 들어갔기 때문에 해당 람다는 Function 타입으로 사용된다.
// Function 인테페이스의 apply 메서드는 T 타입을 파라미터로 받아 R 타입으로 반환한다.
// 사용된 람다에서는 String 타입이 파라미터로 T에 대입되고, String.length()는 int를 반환하므로 Integer 타입이 R에 대입된다.
map(Arrays.asList("asdfasg", "asda", "qrqfasqwdasd"), (String s) -> s.length());

// 컴파일러는 람다 표현식의 파라미터 형식에 접근할 수 있기 때문에 아래와 같이 람다 파라미터 형식을 추론할 수도 있다.
map(Arrays.asList("asdfasg", "asda", "qrqfasqwdasd"), (s) -> s.length());

// 메서드 참조를 이용하면 기존의 메서드 정의를 재활용하여 람다처럼 전달할 수 있다.
// String의 length() 메서드를 참조하는 예이다.
map(Arrays.asList("asdfasg", "asda", "qrqfasqwdasd"), String::length);
```


몇몇 함수형 인터페이스(`Comparator`, `Function`, `Predicate` 등)는 람다 표현식을 조합하여 사용할 수 있도록 유틸리티 메서드인 `Default` 메서드를 제공한다. `Comparator`의 `reversed()`, `thenComparing()` 등이 그 예로, 이들을 이용하여 이후 동작을 정의하거나 람다를 조합하여 사용할 수 있다. 아래는 `thenComparing()`을 사용한 예이다.

```java
/*
아래 둘은 동일한 결과를 갖는다.
*/

Arrays.sort(a, (o1, o2) -> {
    int length1 = o1.getLength();
    int length2 = o2.getLength();
    if (length1 == length2) {
        return o1.getStartTime() - o2.getStartTime();
    }
    return length1 - length2;
});

Arrays.sort(a,
        Comparator.comparing(Meeting::getLength)
                .thenComparing(Meeting::getStartTime));
```

