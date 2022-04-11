# temp

## JWT를 이용해 소셜 로그인 구현
- Spring Security
- OAuth2
- 참고 사이트 : https://earth-95.tistory.com/105
- https://ozofweird.tistory.com/entry/Spring-Boot-Spring-Boot-JWT-OAuth2-2


- spring-boot-starter-security
- spring-boot-starter-oauth2-client
- 차이는??

```java
@Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable() // h2 console 접속을 위해
            .headers().frameOptions().disable() // h2 console 접속을 위해
            .and()
            .oauth2Login() // OAuth2 로그인 설정 시작점
            .userInfoEndpoint() // OAuth2 로그인 성공 이후 사용자 정보를 가져올 때 설정 담당
            .userService(oAuthService); // OAuth2 로그인 성공 시, 후작업을 진행할 UserService 인터페이스 구현체 등록
    }
```
- csrf는 뭔지
- frameOptions는 뭔지
- 공부할것



- access token을 가져오거나, 유저 정보를 가져올 때는 실제로 OAuth 서버와 통신을 해야한다. WebClient를 사용하여 통신을 하려고한다. 아래의 의존성을 추가해주자. 
- `implementation 'org.springframework.boot:spring-boot-starter-webflux'`


- 한번만 되고 DB에 저장이 안된다..
- redirect url 변경해서 그렇다. /해결



- inMemoryAuthentication()
- 인증 설정을 만든다.
- 인메모리 사용자 저장소
- 인메모리 사용자 저장소가 디버깅이나 개발 테스트 목적으로만 유용



- addViewController


---

## 오락가락 하지말자.. 다시..

- 리액트와 스프링으로 소셜로그인을 구현한다.
- application.yml 작성
- AppProperties 바인딩
- AppProperties 활성화
- Cors 활성화 - 프론트에서 엑세스할 수 있도록
- User Entity, Repository 작성
- SecurityConfig 작성


- 실패. 추후 다시공부 후 수정


## JPA & QueryDSL
- Querydsl로 쿼리 작성하면서 애를 먹었다.
- QType으로 변환한 엔티티에 ENUM 타입의 멤버 변수가 있었다.
- QType의 엔티티에서 해당 멤버변수를 DTO에 바로 집어넣고 이를 `.name` 등으로 `String`타입으로 변환하려고 하니 변환할 수 없다고 에러가 발생했다.
- 이 때, 나는 `Projections.fields`를 이용해 접근하고 있었다.
- 이를 `@QueryProjection`를 통해 해결 해주었다.
- QType으로 변환하여 발생하는 문제라고 생각하여 해당 결과를 받아올 DTO도 QType으로 변환하였다.
- 아직 원인을 발견하지 못했다. 더 공부하면서 원인을 찾아 공부하고 다시 기록할 예정이다.

### SQL
- ERROR o.h.e.jdbc.spi.SqlExceptionHelper - Zero date value prohibited
- Mysql에서 timestamp 컬럼 값을 조회할 때 zero date로 저장되어 있는 값을 java localDate로 변환하면서 발생한다.
- Mysql의 zero date는 날짜 형식 컬럼에 값을 저장할 때 오류가 발생하면 해당 형식으로 저장하고 valid date로 처리한다.
- 하지만 자바에서 zero date는 표현할 수 없는 값이다.
- 따라서 datasource에서 jdbc url 뒤에 `zeroDateTimeBehavior=convertToNull` 옵션을 붙여준다.
- zero date를 null로 변환하도록 해준다.


---

## 스프링 - 리액트 채팅 구현
- Web-Socket 사용
- HTTP 1.1
- STOMP
- https://dodop-blog.tistory.com/227
- https://dev-gorany.tistory.com/212



## stomp 채팅 구현
- WebSocketConfig
  - `configureMessageBroker`
    - `setApplicationDestinationPrefixes`
    - 서버에서 클라이언트로부터 메세지를 받을 api의 prefix 설정
    - `enableSimpleBroker`
    - 메모리 기반 메세지 브로커가 해당 api를 구독하고 있는 클라이언트에게 메세지 전달.


## RestTemplate
```java
String baseUrl = "localhost:8088/api/v1/test";

RestTemplate restTemplate = new RestTemplate();

ResponseEntity<String> response = restTemplate.getForEntity(baseUrl, String.class);
```
- getForEntity를 사용하면 위와같이 ResponseEntity 객체를 return 받을 수 있습니다.
- https://dev-alxndr.tistory.com/10