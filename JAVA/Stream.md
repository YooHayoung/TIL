# Stream

## 스트림이란
스트림(Stream)은 자바 8 API에 새로 추가된 기능으로 스트림을 이용하면 선언형으로 컬렉션 데이터를 처리할 수 있다. 선언형으로 처리한다는 말은 데이터를 처리하는 임시 구현 코드 대신 질의로 표현할 수 있다는 것을 말한다. 
아래는 스트림의 정의이다.

- 스트림(Steam)이란 `데이터 처리 연산`을 지원하도록 `소스`에서 추출된 `연속된 요소`로 정의할 수 있다.

스트림은 컬렉션과 같이 특정 요소 형식으로 이루어진 연속된 값 집합의 인터페이스를 제공한다. 컬렉션은 자료구조로 요소의 저장 및 접근 연산이 주를 이루는 반면, 스트림은 표현 계산식이 주를 이룬다. 컬렉션의 주제는 데이터이고, 스트림의 주제는 계산인 것으로 볼 수 있다.

스트림은 컬렉션, 배열, IO 자원 등의 데이터를 제공하는 소스(Source)로부터 데이터를 소비한다. 따라서 정렬된 컬랙션으로 스트림을 생성하면 스트림은 해당 컬렉션을 소비하는 것이기 때문에 정렬이 그대로 유지된다.

스트림은 함수형 프로그래밍 언어에서 일반적으로 지원하는 연산과 데이터베이스와 비슷한 연산을 지원한다. `filter`, `map`, `reduce`, `find`, `match`, `sort` 등으로 데이터를 조작할 수 있다.

또한 스트림은 **파이프라이닝**과 **내부 반복**이라는 중요한 특징을 가지고 있다.
- **파이프라이닝**은 스트림 연산끼리 연결하여 커다란 파이프 라인을 구성할 수 있도록 하는 것이다. 대부분의 스트림 연산은 스트림 자신을 반환하기 때문에 파이프라이닝이 가능하다. 이를 통해 쇼트서킷과 같은 최적화도 얻을 수 있다.
- **내부 반복**은 명시적으로 반복자를 통해 반복을 하지 않고, 스트림 내부에서 일어나는 반복을 말한다. 컬렉션은 반복자를 이용하여 명시적으로 반복을 하지만, 스트림은 내부에서 반복이 일어나는 연산들을 지원하기 때문에 명시적으로 반복을 할 필요가 없다.

아래 코드는 컬렉션을 반복자를 통해 필터링하는 코드이다.

```java
// members 변수는 여러 Member 객체를 담은 컬렉션이다.
// teenager 변수는 20살 아래는 Member 객체를 담을 컬렉션이다.
List<Member> teenagers = new ArrayList<>();
for (Member member : members) {
    if(member.getAge() < 20) {
        teenagers.add(member);
    }
}

List<String> teenagerNames = new ArrayList<>();
for (Member teenager : teenagers) {
    teenagerNames.add(teenager.getName());
}
```

위 코드를 스트림을 이용하면 다음과 같이 변환할 수 있다.

```java
// members 변수는 여러 Member 객체를 담은 컬렉션이다.
// 해당 스트림 연산에서 데이터 소스는 members 컬렉션이다.
List<String> teenagerNames = members.stream()
        .filter(member -> member.getAge() < 20) // 내부 반복
        .map(Member::getName) // 파이프라이닝이 가능하다. 내부 반복
        .collect(toList());
```



## 스트림과 컬렉션의 차이
컬렉션과 스트림 모두 연속된 요소 형식의 값을 저장하는 자료구조의 인터페이스를 제공한다는 공통점이 있다. 하지만 컬렉션과 스트림은 다음과 같은 차이점 또한 가진다.

### 데이터 처리 시점의 차이
컬렉션은 현재 자료구조가 포함하는 모든 값을 메모리에 저장한다. 따라서 컬렉션의 모든 요소는 컬렉션에 추가하기 전에 계산되어야 한다.

반면 스트림은 이론적으로 요청할 때만 요소를 계산한다. 사용자가 요청하는 값만 스트림에서 추출하는 것이다. (생산자-소비자 구조)

### 데이터 탐색에서의 차이
또한 컬렉션은 메모리에 저장되기 때문에 반복적으로 탐색이 가능하다. 반면 스트림에서는, 한번 탐색된 스트림의 요소는 소비되기 때문에 스트림은 단 한 번만 탐색할 수 있다.

### 데이터 반복 처리 방법의 차이
컬렉션 인터페이스를 사용하려면 사용자가 직접 요소를 반복해야 한다. 이를 외부 반복이라고 한다.

```java
// members 는 Member 객체를 요소로 가진 컬렉션이다.
List<String> names = new ArrayList<>();
for (Member member : members) {
    members.add(member.getName);
}
```

반면 스트림을 내부 반복을 사용하기 때문에 어떤 작업을 수행할지만 지정하면 알아서 처리된다.

```java
// members 는 Member 객체를 요소로 가진 컬렉션이다.
List<String> names = members.stream()
        .map(Member::getName)
        .collect(Collectors.toList());
```

스트림과 같이 내부 반복을 이용하면 작업을 투명하게 병렬로 처리하거나 더 최적화된 다양한 순서로 처리할 수 있다. 또한 외부 반복에서는 병렬성을 스스로 관리해야 하지만, 스트림 라이브러리에서는 내부 반복 과정에서 데이터 표현과 하드웨어를 활용한 병렬성 구현을 자동으로 선택한다.

## 스트림의 연산
스트림의 연산은 **중간 연산**과 **최종 연산**으로 구분할 수 있다. 

**중간 연산**은 스트림을 연결할 수 있는 연산을 말하는데 `filter`, `sorted`와 같은 연산이 있다. 중간 연산은 다른 스트림을 반환하기 때문에 다음과 같이 여러 중간 연산을 연결하여 질의를 만들 수 있다.

```java
members.stream().
    .filter(...) // 중간연산
    .map(...) // 중간연산
    .limit(...) // 중간연산
    .collect(toList()); // 최종연산
```

중간 연산은 해당 단말 연산을 스트림 파이프라인에 실행하기 전까지는 아무 연산도 실행하지 않는다는 중요한 특징을 갖는다. 중간 연산을 모두 합친 다음에 합쳐진 중간 연산을 최종 연산으로 한번에 처리한다.

위 코드에서 `filter()`, `map()`, `limit()`을 순차적으로 수행하는 것이 아니라 이를 모두 합친 하나의 연산으로 수행된다. 이를 루프 퓨전이라고 한다.

**최종 연산**은 스트림을 닫는 연산을 말한다. 보통 최종 연산에 의해 `List`, `Integer`, `void` 등 스트림 이외의 결과가 반환된다. `forEach()`, `collect()` 등이 최종 연산으로 `forEach()`는 `void`를 반환하고, `collect()`는 스트림을 컬렉션으로 변환하여 반환한다.

따라서 스트림의 이용 과정은 다음과 같이 세 단계로 나누어 볼 수 있다.
1. 질의를 수행할 데이터 소스를 지정한다.
2. 스트림 파이프라인을 구성할 중간 연산을 연결한다.
3. 스트림 파이프라인을 실행하고 결과를 만들 최종 연산을 지정한다.

```java
members.stream(). // 1. 데이터 소스를 members 컬렉션으로 지정하고, stream으로 변환한다.
    .filter(...) // 2. 중간연산
    .map(...) // 2. 중간연산
    .limit(...) // 2. 중간연산
    .collect(toList()); // 3. 최종연산을 통해 스트림을 닫고, 결과를 반환한다.
```


## 스트림의 메서드 사용법

### 필터링
스트림 인터페이스는 필터링을 위해 `filter` 메서드와 `distinct` 메서드를 지원한다.

`filter` 메서드는 `Predicate`를 인수로 받아서 이와 일치하는 모든 요소를 포함하는 스트림을 반환한다. `Predicate`는 `Boolean`을 반환하는 함수형 인터페이스를 말한다.

```java
List<Member> filteringMembers = 
    memberList.stream()
        // name이 yoo와 일치하는 Member 객체만 필터링한다.
        .filter(member -> member.getName.equals("yoo"))
        .collect(Collectors.toList());
```

`distinct` 메서드는 스트림에서 만든 객체의 `hashCode`와 `equals`를 통해 고유 요소를 판단하여 중복을 제거한 스트림을 반환한다.

```java
List<Member> filteringMembers = 
    memberList.stream()
        .distinct() // 동일한 값을 가진 객체를 제거한 스트림을 반환한다.
        .collect(Collectors.toList());
```

### 슬라이싱
스트림의 슬라이싱은 스트림의 요소를 선택하거나 스킵하는 것을 말한다. 스트림 인터페이스는 슬라이싱을 위해 `takeWhile`, `dropWhile`, `limit`, `skip` 메서드를 지원한다.

`takeWhile` 메서드는 `Predicate`를 인수로 받아서 `Predicate`가 거짓이 되기 전 까지의 요소를 선택하여 반환한다.
`dropWhile` 메서드는 `takeWhile` 메서드와는 반대로, `Predicate`를 인수로 받아서 `Predicate`가 거짓이 되는 지점까지의 요소를 버리고, 이후의 요소를 선택하여 반환한다.

이미 정렬된 데이터에서 특정 지점 이전 또는 이후의 값들을 선택하고자 할 때, `filter` 메서드를 이용하면 전체 요소에 `Predicate`를 적용하여 시간이 오래걸릴 수 있다. 반면 `takeWhile`, `dropWhile` 메서드를 이용하면 전체 요소에 이를 적용하지 않고 `Predicate`가 거짓이 되면 즉시 작업을 중단하고 결과를 반환하기 때문에 소요 시간을 줄일 수 있다.

```java
List<Member> sliceMembers = 
    // memberList가 나이 순으로 정렬되어 있다고 가정한다.
    memberList.stream()
        .takeWhile(member -> member.getAge() < 20)
        .collect(Collectors.toList());
```

`limit` 메서드는 `long` 값을 인수로 받아서 해당 값 이하의 크기를 갖는 새로운 스트림을 반환한다. 스트림의 처음부터 최대 주어진 값까지의 결과를 선택한 스트림을 반환한다.
`skip` 메서드는 `long` 값을 인수로 받아서 스트림의 처음부터 주어진 값만큼의 요소를 제외한 스트림을 반환한다.

```java
// limit 사용
List<Member> sliceMembers = 
    memberList.stream()
        .filter(member -> member.getAge() < 20)
        .limit(3) // 스트림의 처음부터 최대 3개까지 선택한 스트림을 반환한다.
        .collect(Collectors.toList());

// skip 사용
List<Member> sliceMembers2 = 
    memberList.stream()
        .filter(member -> member.getAge() < 20)
        .skip(2) // 스트림의 처음부터 2개를 제외한 스트림을 반환한다.
        .collect(Collectors.toList());
```

### 매핑
스트림 인터페이스는 특정 객체에서 특정 데이터를 선택하는 작업을 위해 `map`과 `flatMap` 메서드를 제공한다.

`map`과 `flatMap` 메서드는 `Function`을 인수로 받아서 스트림의 각 요소에 적용하고, 이를 적용한 결과들을 통해 새로운 요소로 매핑한다. `Function`은 함수형 인터페이스로 `T` 타입의 객체를 사용하여 `R` 타입의 결과를 반환한다. 

여기서 `flatMap` 메서드는 스트림을 평면화한다. 스트림의 각 값을 다른 스트림으로 만든 다음에 모든 스트림을 하나의 스트림으로 연결하는 기능을 수행한다.

```java
String[] words = {"Hello", "World"};

List<String> chars = 
    words.stream()
        // map을 통해 String -> String[]으로 매핑한다.
        // Stream<String> -> Stream<String[]>
        .map(word -> word.split(""))
        // 인수로 전달받은 Function 함수형 인터페이스는 String[] -> Stream<String>을 수행한다.
        // flatMap 메서드는 Function의 각 요소에 대한 결과 Stream<String>을
        // 하나의 Stream<String>으로 매핑한다.
        .flatMap(Arrays::stream)
        .collect(Collectors.toList());
```

### 매칭
스트림 인터페이스는 해당 스트림이 어떤 조건에 매칭되는지 검사하도록 하는 `anyMatch`, `allMatch`, `noneMatch` 메서드를 제공한다. 해당 메서드들은 `Predicate`를 인수로 받는다. 이들은 `Boolean`을 반환하기 때문에 최종 연산이다.

`anyMatch`는 스트림에서 인수로 받은 `Predicate`에 적어도 하나 이상의 요소와 일치하는지 확인한다. 하나라도 일치하면 `true`를 반환한다.

`allMatch`는 스트림의 모든 요소가 인수로 받은 `Predicate`와 일치하는지 검사한다. 모두 일치하면 `true`, 하나라도 일치하지 않으면 `false`를 반환한다.

`noneMatch`는 스트림에서 주이전 `Predicate`와 일치하는 요소가 없는지 확인한다. 모두 일치하지 않으면 `true`를, 하나라도 일치하면 `false`를 반환한다. `allMatch`와는 반대의 연산을 수행한다.

```java
List<Member> memberList = Arrays.asList(
    new Member("member1", 20),
    new Member("member2", 19),
    new Member("member3", 18),
    new Member("member4", 15)
);

// anyMatch : member1을 제외한 나머지가 20살 이하이다. true를 반환한다.
boolean isTeenagerIn = memberList.stream().anyMatch(member -> member.getAge() < 20);

// allMatch : member1이 20살이다. 모든 요소가 조건을 만족해야 true, 그렇지 않으면 false를 반환.
// 여기서는 모든 요소가 조건을 만족하지 못하였기 때문에 false를 반환한다.
boolean isTeenagerAll = memberList.stream().allMatch(member -> member.getAge() < 20);

// noneMatch : member1을 제외한 나머지가 20살 이하이다. noneMatch는 스트림의 모든 요소가 해당 조건을 만족하지 않아야 한다.
// 여기서는 false를 반환한다.
boolean isNotTeenagerIn = memberList.stream().noneMatch(member -> member.getAge() < 20);
```

### 검색
스트림 인터페이스는 스트림에서 요소 검색을 위해 `findAny`와 `findFirst` 메서드를 제공한다. `findAny` 메서드는 현재 스트림의 임의의 요소 하나를 반환한다. `findFirst` 메서드는 현재 스트림의 첫 번째 요소를 반환한다. 해당 메서드들은 스트림이 비어있을 수 있기 때문에 `Optional<T>`를 반환한다. 이들 메서드는 스트림에서 `Optional<T>` 요소를 반환하기 때문에 최종 연산이다.

> `findAny`와 `findFirst` 메서드를 모두 지원하는 이유는 병렬성 때문이다. 병렬 실행에서는 첫 번째 요소를 찾기 어렵기 때문에 요소의 반환 순서가 상관이 없다면 병렬 스트림에서는 제약이 적은 `findAny`를 사용한다.

```java
Optinal<Member> findMember = 
    memberList.stream()
        // name이 yoo와 일치하는 Member 객체만 필터링한다.
        .filter(member -> member.getName.equals("yoo"))
        // filter 메서드를 통해 반환받은 Stream<Member>에서 임의의 하나의 Member를 반환한다.
        // Stream<Member>가 비어있을 수 있기 때문에 Optional<Member>를 반환한다.
        .findAny();
```

### 리듀싱
스트림에서 리듀싱 연산(`reduce()`)은 모든 스트림 요소를 처리하여 값으로 도출하는 것을 말한다. "회원 중에서 가장 나이가 많은 사람은 누구인가"와 같이 스트림의 모든 요소를 처리하여 최종적으로 하나의 값을 반환하도록 한다. 하나의 값으로 처리하기 때문에 최종 연산이다.

`reduce` 메서드는 두 개의 인수(스트림의 각 요소와 함께 사용할 초기값, 두 요소를 조합하여 새로운 값을 만드는 `BinaryOperator` 함수형 인터페이스)를 갖는다.

초기값을 받지 않도록 오버로드된 `reduce`도 있다. 이는 스트림에 아무 요소도 없을 경우에 초기값이 존재하지 않기 때문에 `Optional` 객체를 반환한다.

```java
// 초기값을 주면 (초기값, 스트림의 첫번째 요소) 부터 시작한다.
Integer reduce1 = Arrays.asList(1, 2, 3).stream()
    .reduce(1, (a, b) -> a * b + 3); // 36

// 초기값을 주지 않으면 (스트림의 첫번째 요소, 스트림의 두번째 요소) 부터 시작한다.
Optional<Integer> reduce2 = Arrays.asList(1, 2, 3).stream()
    .reduce((a, b) -> a * b + 3); // 18
```

스트림은 공통적인 리듀스 패턴에 사용할 수 있도록 `min`, `max` 내장 메서드를 제공한다. 이들은 최댓값이나 최솟값을 계산하는데 사용할 키를 지정하는 `Comparator`를 인수로 받는다.

```java
Integer minAge = members.stream()
    .min(Comparator.comparing(Member::getAge)); // 회원 중 최소 나이
```

### 기본형 특화 스트림
스트림은 숫자 스트림을 효율적으로 처리할 수 있도록 `IntStream`, `DoubleStream`, `LongStream`을 제공한다. 이들은 숫자 스트림의 합계를 계산하는 `sum`, 최대값 요소를 검색하는 `max`, 요소들의 평균값을 계산하는 `average` 등과 같이 자주 사용하는 숫자 관련 리듀싱 연산 수행 메서드를 제공한다. 또한 필요할 때 기본형 값을 다시 객체 스트림으로 복원하도록 `boxed` 메서드를 제공한다.

```java
IntStream intStream = memberList.stream()
    .mapToInt(Member::getAge); // mapToInt는 IntStream을 반환한다.

Stream<Integer> boxed = memberList.stream()
    .mapToInt(Member::getAge)
    .boxed(); // boxed를 통해 IntStream을 Stream<Integer>로 다시 박싱할 수 있다.

OptionalDouble average = memberList.stream()
    .mapToInt(Member::getAge)
    .average(); // IntStream 등의 기본형 스트림은 average와 같은 다양한 유틸리티 메서드를 지원한다.

// OptionalDouble은 getAsDouble 등과 같이 꺼내어 사용할 수 있다.
System.out.println(average.getAsDouble());
// Stream이 비어있어서 average 값이 없는 상황에는 다음과 같이 기본값을 지정할 수 있다.
System.out.println(average.orElse(0));
```

#### 5.7.2 숫자 범위
...여기부터 시작...