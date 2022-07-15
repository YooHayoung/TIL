# 타임리프
## 타임리프 특징
- Server Side Rendering (SSR)
- 네츄럴 템플릿
	- 순수 HTML을 유지하면서 뷰 템플릿도 사용 가능
- 스프링 통합 지원

## 타임리프 사용 선언
`<html xmlns:th="http://www.thymeleaf.org>`

## 기본 표현식
```markdown
- 간단한 표현
  - 변수 표현식 : `${...}`
  - 선택 변수 표현식 : `*{...}`
  - 메시지 표현식 : `#{...}`
  - 링크 URL 표현식 : `@{...}`
  - 조각 표현식 : `~{...}`
- 리터럴
  - 텍스트 : `'...’`
  - 숫자
  - 불린
  - 널
  - 리터럴 토큰 : `one`, `sometext`, `main`, …
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
```


### 텍스트 출력
- HTML 컨텐츠에 데이터 출력 : `th:text`
	- `<span th:text="${data}">`
- HTML 컨텐츠 영역 내에서 직접 데이터를 출력 : `[[...]]`
	 - `<b>My name is [[${data}]]</b>`
- `th:text`, `[[...]]`은 **기본적으로 이스케이프를 제공**
	- Escape : HTML에서 사용하는 특수문자(`<`, `>`)를 HTML 엔티티(`&lt;`, `&gt;`)로 변경하는 것을 Escape라고 함
- Escape 기능을 사용하지 않으려면 `th:utext`, `[(...)]` 사용

### 변수 표현식
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
- 지역변수
	- `th:with`
	- 지역 변수는 선언한 태그 안에서만 사용 가능
```html
<ul th:with="firstUser = ${users[0]}">
	<li th:text="${user.username}"></li>
	<li th:text="${users[0]['username']}"></li>
	<li th:text="${userMap['userA'].getUsername()}"></li>
	<li th:text="${firstUser.username}"></li>
</ul>
```


### 기본 객체
- `${#request}` : `HttpServletRequest` 객체를 그대로 제공
	- HTTP 요청 파라미터 : `param`, `${param.paramData}`
	- HTTP 세션 : `session`, `${session.sessionData}`
	- 스프링 Bean : `@`, `${@helloBean.hello('spring')}`
- `${#response}`
- `${#session}`
- `${#servletContext}`
- `${#locale}`

### 유틸리티 객체
- `#message` : 메시지, 국제화 처리
- `#uris` : URI 이스케이프 지원
- `#dates` : `java.util.Date` 지원
- `#calendars` : `java.util.Calendar` 지원
- `#temporals` : java8 날짜 서식
	- `thymeleaf-extras-java8time` 라이브러리
- `#numbers` : 숫자 서식
- `#strings` : 문자 관련 편의 기능
- `#objects` : 객체 관련 기능
- `#bools` : 불린 관련 기능
- `#arrays` : 배열 관련 기능
- `#lists`, `#sets`, `#maps` : 컬렉션 관련 기능
- `#ids` : 아이디 처리 관련 기능

> 타임리프 유틸리티 객체 -> https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#expression-utility-objects
> 유틸리티 객체 예시 -> https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#appendix-b-expression-utility-objects


### URL 링크
- URL 생성시 `@{url}`
	 - `<a th:href="@{/hello}">hello</a>`
	 - `@{/hello/{param1}(param1=${param1}, param2=${param2})}`
	 - -> `/hello/param1?param2=param2`

### 리터럴
- 소스코드상에 고정된 값을 말하는 용어
- 공백을 포함한 문자 리터럴은 작은 따옴표로 감싸야 한다.
	 - `<span th:text="'hello world'">`
	 - `<span th:text="hello">`
- 리터럴 대체 문법이 있다.
 - `th:text="|hello ${data}|"`


### 속성값
- `th:속성="속성값"` : 속성 생성 or 대체
- `th:attrappend` : 속성 값 뒤에 값을 추가
- `th:attrprepend` : 속성 값 앞에 추가
- `th:classapend` : class 속성에 자연스레 추가

```html
<input type="text" name="asd" th:name="nameA" />
<span class="sp1" th:attrappend="class=' large'"></span>
<input type="checkbox" name="active" th:checked="false" />
```


### 반복
- `th:each="user : ${users}"`
	- 두번째 파라미터 -> 반복 상태(생략가능. 생략하면 `지정한 변수명` + `Stat`) 
	 - `th:each="user, userStat : ${users}"`
	 - `-Stat.index` : 시작값 0
	 - `-Stat.count` : 시작값 1
	 - `-Stat.size` : 전체 사이즈
	 - `-Stat.even`, `-Stat.odd` : 홀짝 여부. `boolean`값
	 - `-Stat.first`, `-Stat.last` : 처음, 마지막 여부
	 - `-Stat.current` : 현재 객체


### 조건문
- `if`, `unless`
	 - `th:if="${user.age lt 20}"`
	 - `th:unless="${user.age ge 20}"`
	 - 조건을 만족할 때에만 동작
- `swith`, `case`
```html
<td th:switch="${user.age}"> 
	<tr th:case="10">10</tr> 
	<tr th:case="20">20</tr> <!--/*--> 렌더링시 주석 안보임 <!--*/-->
	<tr th:case="*">else</tr> <!--/*/ ssr시 렌더링, 아니면 주석처리 /*/-->
<!-- HTML 주석. 소스에 주석처리 -->
<!--/* 타임리프 파서 주석. 소스에서도 주석처리 */=-->
<!--/*--> 타임리프 파서 주석. 소스에서도 주석처리 <!--*/-->
<!--/*/ 타임리프 프로토타입 주석. ssr시 렌더링, 아니면 주석처리 /*/-->
</td>
```


### block
- `<th:block>`
- 타임리프의 유일한 자체 태그
- 렌더링시 제거된다.
- `each` 만으로 해결하기 어려울 때 사용된다.
```html
<th:block th:each="user : ${users}">
	<div>
		<span th:text="${user.username}"></span>
		<span th:text="${user.age}"></span>
	</div>
</th:block>
```


### Javascript Inline
- `<script th:inline="javascript"></script>`
- 자바스크립트에서 타임리프를 편리하게 사용
- 반복문 each
```html
<script th:inline="javascript">
	[# th:each="user, userStat : ${users}"]
	let user[[${userStat.count}]] = [[${user}]];
	[/]
</script>
```


### Template fragment
```html
<header th:fragment="fragHeader">
	fragment1
</header>

<footer th:fragment="fragFooter (param1, param2)">
	<p>paramFragment</p>
	<p th:text="${param1}"></p>
	<p th:text="${param2}"></p>
</footer>
```
- 파일을 조각내어 불러올 수 있게 한다. 위에서 `fragHeader`와 `fragFooter`로 코드조각에 이름을 붙여주었다.
- 만들어진 코드 조각은 `th:insert`와 `th:replace`를 통해 사용 가능
```html
<!-- th:insert는 태그 내부에 fragment 삽입 -->
<div th:insert="template/fragment/footer :: fragHeader">
</div>

<!-- replace는 태그를 대체함 -->
<div th:replace="~{template/fragment/footer :: fragFooter ('파라미터1', '파라미터2')}">
</div>
```
 


### 템플릿 레이아웃
- 코드 조각을 레이아웃에 넘겨서 사용
- 코드 조각에 코드를 추가해서 사용
- 레이아웃을 만들어 두고,
- 사용하는 곳에서 파라미터를 통해 전달해서 채운다.
- `fragmentName(~{::title}, ~{::link})`
  - 현재 페이지의 title 태그들 전달
  - 현재 페이지의 link 태그들을 전달
- 이를 html 전체에 적용할 수도 있음




## 타임리프 - 스프링 통합
- 기본 메뉴얼
	- https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html
- 스프링 통합 메뉴얼
	- https://www.thymeleaf.org/doc/tutorials/3.0/thymeleafspring.html 
- 스프링 부트에서 제공하는 타임리프 설정
	- https://docs.spring.io/spring-boot/docs/current/reference/html/appendix-application-properties.html#common-application-properties-templating -> thymeleaf 검색

### 입력 Form
- `th:object` : 커맨드 객체 지정
- `*{...}` : 선택 변수 식. `th:object`에서 지정한 객체에 접근
	- `${객체.객체의 속성}`과 같음
- `th:field` : HTML 태그의 id, name, value 속성을 자동으로 처리
```html
<form action="item.html" th:action th:object="${item}" method="post">
	<input type="text" id="itemName" th:field="*{itemName}" class="form-control" />
</form>
```
-> `<input type="text" id="itemName값" name="itemName값" value="itemName값" class="form-control" />`


### 체크 박스
- HTML에서 체크 박스를 선택하지 않고 폼 전송시 해당 필드 자체가 전송되지 않는다. 서버에서 로그를 남겨보면 `null`로 표시됨.
- 이를 해결하여 `false`로 전송하기 위해서는 `<input type="hidden" name="_fieldName"/>` 필드를 전송하면 스프링에서는 체크를 해제했다고 판단하고 false로 처리한다.
- `th:field`를 이용하면 타임리프는 자동으로 체크박스의 히든 필드를 생성해준다.
```html
<form action="item.html" th:action th:object="${item}" method="post">
	<input type="checkbox" id="open" class="form-check-input" th:field="*{open}" />
	<!-- <input type="hidden" name="_open" value="on"/> 자동 생성 -->
</form>
```

- 체크박스가 여러개인 경우
```html
<form action="item.html" th:action th:object="${item}" method="post">
<div th:each="region : ${regions}" class"...">
	<input type="checkbox" th:field="*{regions}" th:value="${region.key}" class="..." />
</div>
</form>
```

### 라디오 버튼, 셀렉트 박스
- 체크 박스와 사용법은 동일


## 메시지
- 메시지 : 하드코딩된 단어? 문장? 정보?
- 다양한 메시지를 수정하려면 여러 파일을 수정해야 함 -> 메시지를 한 곳에서 관리하면 편리하다.
- `messages.properties`라는 메시지 관리용 파일을 만들어서 값을 저장해둔다.
```properties
hello=안녕
hello.name=안녕 {0}
```

### 스프링 메시지 소스 설정
- `MessageSource`를 스프링 빈으로 등록
	- 이는 인터페이스라서 구현체를 등록해줘야 한다. `ResourceBundleMessageSource`
- 스프링 부트는 스프링이 자동으로 등록한다.
	- `application.properties`에 설정
		- `spring.messages.basename=messages,config.i18n.messages`
		- 별도 설정 없으면 `messages`로 기본 등록

### 메시지 소스 사용
- 테스트시 `MessageSource` 인터페이스의 `getMaeesage` 메소드 이용
- 타임리프에 메시지 표현식 `#{...}`을 사용하여 메시지 조회
	- 파라미터 사용 -> `<span th:text="#{hello.name(${item.itemName})}"></span>`


## 국제화
- 메시지 파일을 각 나라별로 별도로 관리하여 서비스
- `messages_en.properties`, `messages_ko.properties` 등
- `Locale` 정보를 통해 언어 선택. 스프링은 기본으로 `Accept-Language` 헤더 값 사용
- 스프링은 `Locale` 선택 방식을 변경할 수 있도록 `LocalResolver` 인터페이스 제공
	- `Accept-Language`를 활용하는 `AcceptHeaderLocalResolver` 사용
- `Local` 선택 방식을 변경하려면 `LocalResolver`의 구현체를 변경해서 쿠키나 세션 기반의 `Local` 선택 기능 사용 가능




#스프링 MVC/Thymleaf#
#스프링 MVC/Thymleaf/문법#
#스프링 MVC/Thymleaf/스프링 통합#
#스프링 MVC/Thymleaf/메시지#
#스프링 MVC/Thymleaf/국제화#
---
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.