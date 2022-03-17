# 스프링 부트와 AWS로 혼자 구현하는 웹 서비스
*스프링 부트와 AWS로 혼자 구현하는 웹 서비스*를 읽고 정리한 내용입니다.<br>


## 테스트 코드를 작성하자
먼저, TDD와 단위 테스트는 다르다.<br>
TDD는 테스트가 주도하는 개발, 단위테스트는 TDD의 첫 단계인 기능 단위의 테스트 코드를 작성하는 것이다.<br>
책에서는 TDD가 아닌 단위 테스트 코드를 다룬다.

### 테스트 코드는 왜 작성할까
- 단위 테스트는 개발단계 초기에 문제를 발견하게 도와준다.
- 단위 테스트는 개발자가 나중에 코드를 리펙토링하거나 라이브러리 업그레이드 등에서 기존 기능이 올바르게 동작하는지 확인할 수 있다.
- 단위 테스트는 기능에 대한 불확실성을 감소시킬 수 있다.
- 단위 테스트는 시스템에 대한 실제 문서를 제공한다.
  - 단위 테스트 자체가 문서로 사용할 수 있다.
- 빠른 피드백
- 자동 검증 가능
- 개발자가 만든 기능을 안전하게 보호




```java
// 스프링부트 테스트와 Junit 사이의 연결자 역할
@ExtendWith(SpringExtension.class)
@WebMvcTest(controllers = HelloController.class)
class HelloControllerTest {

    @Autowired
    // Web api 테스트할때 사용. HTTP GET, POST 등 테스트 가능
    private MockMvc mvc; 

    @Test
    public void hello가_리턴된다() throws Exception {
        String hello = "hello";

        // 해당 주소로 HTTP 요청
        mvc.perform(MockMvcRequestBuilders.get("/hello")) 
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.content().string("hello"));
    }

    @Test
    public void helloDto가_리턴된다() throws Exception {
        String name = "helloDto";
        int amount = 100;

        mvc.perform(MockMvcRequestBuilders.get("/hello/dto")
                        // 파라미터 값 설정
                        .param("name", name)
                        .param("amount", String.valueOf(amount)))
                .andExpect(status().isOk())
                // json 응답값 필드별 검증
                .andExpect(jsonPath("$.name", is(name)))
                .andExpect(jsonPath("$.amount", is(amount)));
    }
}
```


## JPA
- 패러다임 불일치 해결
  - RDB는 어떻게 데이터를 저장할지에 초점
  - 반면 객체지향 프로그래밍은 기능과 속성을 한 곳에서 관리
  - 이러한 패러다임 불일치를 해결해주는 역할을 JPA가 한다.
- SQL에 종속적인 개발을 하지 않도록 해준다.
  - 위와같은 이유 때문에 개발자는 SQL을 반복적으로 만들고 유지보수 했다.
  - 하지만 JPA가 중간다리 역할을 함으로써 개발자는 항상 객체지향적으로 코드를 표현할 수 있게 되었다.

## Spring Data JPA
- JPA는 인터페이스. 자바 표준명세서다.
- 이를 이용하려면 구현체가 필요하다.
- 대표적으로 Hibernate, Eclipse Link 등
- 이러한 구현체들을 더 쉽게 사용하고자 추상화시킨 것이 Spring Data JPA

### Why?
- 구현체 교체의 용이성
- 저장소 교체의 용이성

*추상화의 중요성 : 다른 구현체들로 교체가 용이하다. 역할 분리!!*


## Entity 클래스에 절대 Setter 메소드를 만들지 않는다.
- 해당 클래스의 인스턴스 값들이 언제 어디서 변해야 하는지 코드상으로 명확하게 구분할 수 없다.
- 해당 필드 값 병경이 필요하다면?
  - 그 목적과 의도를 나타낼 수 있는 메소드를 추가하자.

## Builder
- 생성자를 이용하면 어떤 필드에 어떤 값이 들어가는지 구분하기 힘들다.
- Builder를 사용하면 이를 명확하게 인지할 수 있다.

## Service는 비즈니스 로직을 처리하는 역할이 아니다.
- Service는 트랜잭션, 도메인 간의 순서 보장의 역할을 한다.
- 비즈니스 로직처리는 Domain에서 한다.
- DDD(도메인 주도 설계)?

## View Layer와 DB Layer의 역할 분리를 철저하게 하자.
- Entity와 DTO(Controller에서 사용)는 꼭 분리해서 사용하자.
- Entity는 DB와 맞닿은 핵심 클래스. 이를 기준으로 테이블 생성, 스키마 변경.
- 화면 변경 때문에 Entity가 바뀌어서는 안된다.
- 이를 위해 View를 위한 클래스인 DTO를 생성하고 여기에 Entity의 데이터를 담아 전송한다.

## JPA Auditing
- 생성일, 수정일 등 자동등록

// 220316

---









---
## 공부하면서 배운 것
- MySQL에서 text와 varchar 차이
  - max size limit
    - text : X, only 65535
    - varchar : O, 1 ~ 65535
  - 저장 byte
    - text : only 2byte
    - varchar : 255 size 이하 = 1byte, 256 size 이상 = 2byte
  - index 가능 여부
    - text : X
    - varchar : O
  - 속도
    - text : disk에 저장. 느리다.
    - varchar : memory에 저장. 빠르다.
