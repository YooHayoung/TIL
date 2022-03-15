# JAVA

## Optional
- Optional 값을 꺼내는 방법
    ```java
    // 나쁜 예
    Optional<Member> member = ...;
    if (member.isPresent()) {
        return member.get();
    } else {
        return null;
    }

    // 좋은 예
    Optional<Member> member = ...;
    return member.orElse(null);

    //////////////////////////////////////////////////////

    // 나쁜 예
    Optional<Member> member = ...;
    if (member.isPresent()) {
        return member.get();
    } else {
        throw new NoSuchElementException();
    }

    // 좋은 예
    Optional<Member> member = ...;
    return member.orElseThrow(() -> new NoSuchElementException());
    ```