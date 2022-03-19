# Thymeleaf 특징

## SSR
- 서버에서 HTML을 동적으로 렌더링

## 네츄럴 템플릿
- 타임리프는 순수 HTML을 최대한 유지하는 특징이 있다.
- 때문에 웹 브라우저에서 파일을 직접 열어도 내용을 확인할 수 있다.
- 순수 HTML을 그대로 유지하면서 뷰 템플릿도 사용할 수 있는 타임리프의 특징을 네츄럴 템플릿이라고 한다.

## 스프링 통합 지원
- 타임리프는 스프링과 자연스러베 통합되고, 스프링의 다양한 기능을 편리하게 사용할 수 있게 지원한다.


---

# Thymeleaf 기본 기능

## 타임리프 사용 선언
`<html xmlns:th="http://www.thymeleaf.org>`

## 기본 표현식
- 간단한 표현
  - 변수 표현식 : `${...}`
  - 선택 변수 표현식 : `*{...}`
  - 메시지 표현식 : `#{...}`
  - 링크 URL 표현식 : `@{...}`
  - 조각 표현식 : `~{...}`
- 리터럴
  - 텍스트 : `'...'`
  - 숫자
  - 불린
  - 널
  - 리터럴 토큰 : `one`, `sometext`, `main`, ...
- 문자 연산
  - 문자 합치기 : `+`
  - 리터럴 대체 : `|The name is ${name}|`
- 산술 연산
- 불린 연산
- 비교와 동등
  - 비교 : `>`, `<,` `>=`, `<=` (gt, lt, ge, le)
  - 동등 연산 : `==`, `!=` (eq, ne)
- 조건 연산
  - (if) ? (then)
  - (if) ? (then) : (else)
  - (value) ?: (defaultValue)
- 특별한 토큰
  - No-Operation : `_`
  - 타임리프가 실행되지 않은 것 처럼 동작
  - HTML의 내용 그대로 출력

## 텍스트
- HTML 컨텐츠에 데이터 출력 : `th:text`
  - `<span th:text="${data}">`
- HTML 컨텐츠 영역 내에서 직접 데이터를 출력 : `[[...]]`
  - `<b>My name is [[${data}]]</b>`

### HTML 엔티티와 Escape
- `<span th:text="Hello <b>Spring!</b>">`
  - `<b>`태그가 그대로 출력된다.
  - 소스보기에서는 `&lt;`로 변경된다.
- 웹 브라우저는 `<`를 HTML 태그의 시작으로 인식함
- 이를 태그의 시작이 아니라 문자로 표현할 수 있는 방법이 필요함.
- 이를 HTML 엔티티라고 한다.
- 이러한 HTML에서 사용하는 특수문자(`<`, `>`)를 HTML 엔티티(`&lt;`, `&gt;`)로 변경하는 것을
- Escape라고 한다.
- `th:text`, `[[...]]`은 기본적으로 이스케이프를 제공한다.

### Unescape
- Escape 기능을 사용하지 않으려면
- `th:utext`, `[(...)]`


## 변수 표현식 - Spring EL
- `${...}`
- Object
  - `user.username`
  - `user['username']`
  - `user.getUsername()`
- List
  - `users[0].username`
  - 위와 동등
- Map
  - `userMap['key'].property`
  - 위와 동등

### 지역 변수 선언
- `th:with`
- 지역 변수는 선언한 태그 안에서만 사용 가능




## 기본 객체들
- `${#request}`
  - `HttpServletRequest`객체가 그대로 제공. 불편
  - 이를 해결하기 위해 편의 객체도 제공
- `${#response}`
- `${#session}`
- `${#servletContext}`
- `${#locale}`

### 편의 객체
- HTTP 요청 파라미터 접근 : `param`
  - `${param.paramData`
- HTTP 세션 접근 : `session`
  - `${session.sessionData}`
- Spring Bean 접근 : `@`
  - `${@helloBean.hello('Spring!')}`


## 유틸리티 객체
- `#message` : 메시지, 국제화 처리
- `#uris` : URI 이스케이프 지원
- `#dates` : `java.util.Date` 지원
- `#calendars` : `java.util.Calendar` 지원
- `#temporals` : java8 날짜 서식
- `#numbers` : 숫자 서식
- `#strings` : 문자 관련 편의 기능
- `#objects` : 객체 관련 기능
- `#bools` : 불린 관련 기능
- `#arrays` : 배열 관련 기능
- `#lists`, `#sets`, `#maps` : 컬렉션 관련 기능
- `#ids` : 아이디 처리 관련 기능


## URL 링크
- URL 생성시에는 `@{...}`문법 사용
  - `<a th:href="@{/hello}">hello</a>`
  - `@{/hello/{param1}(param1=${param1}, param2=${param2})}`
  - `()`안에 있는 부분은 쿼리 파라미터 처리
  - URL 경로상에 변수가 있으면 `()`부분은 경로 변수 처리
  - 혼합 가능


## 리터럴
- 소스코드상에 고정된 값을 말하는 용어
- 문자 리터럴은 작은 따옴표로 감싸야 한다.
  - 공백없으면 생략해도 된다.
  - `th:text="'hello world'"`
- 리터럴 대체 문법이 있다.
  - `th:text="|hello ${data}|"`


## 연산
- HTML 엔티티 사용하는 부분을 주의


## 속성 값 설정
- `th:*` : 속성 적용
  - 기존 속성 대체
  - 없으면 새로 추가
- HTML에서 `checked`속성은 true, false와 상관없이 속성이 있기만 하면 체크된다.
  - `th:checked="false"` : `checked` 속성 자체를 제거


## 반복
- `th:each="user : ${users}"`
- 여러 상태 값 지원
  - `th:each="user, userStat : ${users}"`
  - 반복의 두번째 파라미터를 설정해서 반복 상태 확인 가능
  - 이는 생략 가능. 생략하면 지정한 변수명 + `Stat`이 된다.
  - `index` : 시작값 0
  - `count` : 시작값 1
  - `size` : 전체 사이즈
  - `even`, `odd` : 홀짝 여부. `boolean`값
  - `first`, `last` : 처음, 마지막 여부
  - `current` : 현재 객체


## 조건부 평가
- `if`, `unless`(if 반대)
  - `th:if="${user.age lt 20}"`
  - 해당 조건이 맞지 않으면 태그 자체를 렌더링하지 않음
- `swith`, `case`
  - `*` : 만족하는 조건이 없을때 사용함. Default


## 주석
- HTML 주석
  - `<!--  -->`
- 타임리프 파서 주석
  - `<!--/*  */-->`
  - `<!--/*-->`, `<!--*/-->`
- 타임리프 프로토타입 주석
  - `<!--/*/ ... /*/-->` 
  - HTML 파일을 직접 열면 주석처리
  - 타임리프 렌더링을 거치면 정상 렌더링


## 블록
- `<th:block>`
- HTML 태그가 아님
- 타임리프의 유일한 자체 태그
- 블록 태그는 렌더링시 제거된다.
- `each` 만으로 해결하기 어려울 때 사용된다.


## 자바스크립트 인라인
- `<script th:inline="javascript"></script>`
- 텍스트 렌더링
  - 문자 타입인 경우 큰따옴표 붙여준다.
  - 자바스크립트에서 문제가 될 수 있는 문자가 있으면 이스케이프 처리
  - 자바 `\"` -> `&quot;`
- 자바스크립트 네츄럴 템플릿
- 객체 JSON 변환
- `[# th:each="..."] ... [/]` 지원
  - 반복문. 사용법 동일

### 사용하지 않으면, 
- 변수의 문자같은 경우, `[[...]]`을 통해 가져오면 큰따옴표 없이 그냥 가져와서 error 발생.
  - `"[[]]"`를 통해 해결 가능. 큰따옴표를 붙여주면 된다.
  - or 자바스크립트 인라인을 통해 해결 가능
- `[[]]`로 객체를 가져오면 toString을 호출한다.
  - 자바스크립트 인라인은 객체를 JSON으로 넣어준다.
- 네츄럴 템플릿 지원하지 않는다.


## 템플릿 조각
- 파일을 조각내서 불러올 수 있다.
- `th:fragment`
  - 위 속성이 포함된 태그는 다른 곳에 포함되는 코드 조각임
  - `th:fragment="fragement이름 (param1, param2)"`
  - 다른 곳에서 이름으로 태그를 긁어서 사용할 수 있다.
  - 파라미터도 가능하다.
- `th:insert="~{templates이하 폴더명/파일명 :: fragment이름}"`
  - insert가 포함된 태그 안에 넣는다.
  - `th:replace`도 있다.
  - replace는 태그를 대체한다.


## 템플릿 레이아웃
- 코드 조각을 레이아웃에 넘겨서 사용
- 코드 조각에 코드를 추가해서 사용
- 레이아웃을 만들어 두고,
- 사용하는 곳에서 파라미터를 통해 전달해서 채운다.
- `fragmentName(~{::title}, ~{::link})`
  - 현재 페이지의 title 태그들 전달
  - 현재 페이지의 link 태그들을 전달
- 이를 html 전체에 적용할 수도 있음


---

# 스프링 통합과 폼

















<br><br><br><br>

---

해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.