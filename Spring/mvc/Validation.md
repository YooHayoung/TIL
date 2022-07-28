# Validation

[1. BindingResult](#bindingresult)
[2. Validator : Interface](#validator--interface)
[3. Thymeleaf : BindingResult 사용](#thymeleaf--bindingresult-사용)
[4. Bean Validation](#bean-validation)
[5. API 검증](#api-검증)

---

컨트롤러의 역할은 HTTP 요청이 정상인지 검증하는 것이다. 따라서 검증 로직을 잘 개발해야한다.

HTTP 요청은 클라이언트에서 검증할 수 있고 서버에서도 검증할 수 있다. 클라이언트 검증은 자바스크립트를 통해 프론트 단에서 요청을 보내기 전에 검증하는 것이고 서버 검증은 자바 스프링 등을 통해 서버에서 전송받은 요청을 백 단에서 검증한다.

클라이언트 검증은 조작할 수 있기 때문에 보안에 취약하다. 서버만으로 검증하게 되면 즉각적인 고객 사용성이 부족해진다. 따라서 이 둘을 적절히 잘 섞어서 사용해야 하며 최종적으로 서버 검증은 필수이다. API 방식을 사용하면 API 스펙을 잘 정의하여 검증 오류를 API 응답 결과에 잘 남겨주도록 해야한다.

화면에서 전달받은 데이터를 검증하고, 검증에 성공하면 로직이 정상 수행, 검증에 실패하면 어떤 데이터가 검증에 실패하였는지, 왜 실패하였는지, 사용자가 입력하여 전송한 데이터가 어떤 데이터인지(사용자가 입력한 데이터를 다시 화면에 출력시켜줘야 더 좋은 사용자 경험을 얻을 수 있다.) 알아야 한다.

이를 위해 스프링은 `BindingResult`를 제공하여 검증 오류를 보관할 수 있도록 돕는다.

## BindingResult
`BindingResult` 객체는 스프링이 제공하는 것으로, 검증 오류를 보관하는 객체이다. 검증 과정에서 오류가 발생하면 그 오류가 발생한 필드와 오류에 대한 메시지를 담을 수 있다.

`BindingResult`에 검증 오류를 담으려면 `addError` 메서드를 이용하여 특정 필드나, 객체에 대한 오류를 생성하여 담으면 된다.
특정 필드에 대한 오류는 `FieldError` 객체를 생성, 특정 필드를 넘어서는 오류(객체에 대한 오류)는 `ObjectError` 객체를 생성하고, `BindingResult`의 `addError` 메서드를 통해 추가하면 된다.

`FieldError`와 `ObjectError`는 두가지 생성자를 갖는다. 아래 생성자에서 각 파라미터가 의미하는 것은 다음과 같다.

- `objectName` : 검증 오류가 발생한 객체명
- `field` : 오류가 발생한 객체의 필드명
- `rejectedValue` : 사용자가 입력한 검증 실패한 값. 검증 오류가 발생하면, 이를 통해 사용자가 입력한 값을 화면에 다시 출력할 수 있다.
- `bindingFailure` : 바인딩 실패(타입 오류)이면 `true`, 검증 실패이면 `false`
- `codes` : `messages.properties`에서 가져올 오류 메시지 코드
- `arguments` : 오류 메시지 코드를 통해 가져온 메시지에서 사용할 인자
- `defaultMessage` : `codes`를 통해 가져온 메시지가 없을 때 사용할 기본 오류 메시지

```java
// FieldError
public class FieldError extends ObjectError {

	public FieldError(String objectName, String field, String defaultMessage) { ... }

	public FieldError(String objectName, String field, 
		@Nullable Object rejectedValue, boolean bindingFailure, 
		@Nullable String[] codes, @Nullable Object[] arguments, 
		@Nullable String defaultMessage) { ... }
}

// ObjectError
public class ObjectError extends DefaultMessageSourceResolvable {

	public ObjectError(String objectName, String defaultMessage) { ... }

	public ObjectError(String objectName, @Nullable String[] codes,
		@Nullable Object[] arguments, @Nullable String defaultMessage) { ... }
}
```

다음과 같이 사용하여 `BindingResult`에 검증 오류 정보를 담을 수 있다.

```java
// 특정 필드 오류 - FieldError
// member 객체의 nickname 필드를 입력하지 않으면 검증 실패.
// 검증에 실패하면 BindingResult에 정보를 담는다.
if (!StringUtils.hasText(member.getNickname())) {
	bindingResult.addError(
		new FieldError("member", "nickname", "닉네임을 입력하세요."));
}

// 오류 메시지를 meessages.properties에서 찾는다.
// required.member.nickname 코드의 메시지를 가져온다.
// rejectedValue에 member.getNickname()을 통해 거절된 값을 담는다.
// 기존 화면에서 사용자가 입력한 값을 다시 출력시킬 수 있다.
if (!StringUtils.hasText(member.getNickname())) {
	bindingResult.addError(
		new FieldError("member", "nickname", member.getNickname(),
			false, new String[]{"required.member.nickname"}, null, null)
	);
}

// 객체 오류 - ObjectError
// 특정 필드를 넘어서는 오류는 ObjectError를 생성하여 BindingResult에 담는다.
if (member.getLoginId().equals(member.getPassword())) {
	bindingResult.addError(
		new ObjectError("member", "로그인 이메일과 비밀번호가 일치하면 안됩니다."));
}

// 오류 메시지를 meessages.properties에서 찾는다.
// notEqualsIdAndPassword 코드의 메시지를 가져온다.
if (member.getLoginId().equals(member.getPassword())) {
	bindingResult.addError(
		new ObjectError("member", 
			new String[]{"notEqualsIdAndPassword"}, null, null)
	);
}
```

### reject, rejectValue
`BindingResult`의 `rejectValue`, `reject` 메서드를 사용하면 `FieldError`와 `ObjectError`를 직접 생성하지 않고도 검증 오류를 담을 수 있다. 
`reject`와 `rejectValue` 메서드는 `errorCode`를 인자로 받는다. 여기서 `errorCode`는 `messages.properties`에 등록된 코드가 아니라 `MessageCodesResolver`를 위한 오류 코드이다. 내부에서 `FieldError`, `ObejctError`를 생성하고, `MessageCodesResolver`가 자동으로 `errorCode`를 바탕으로 오류 코드들을 생성한다. `MessageCodesResolver`는 다음과 같은 규칙으로 오류 코드를 자동 생성하고, `messages.properties`에서 순위에 따라 일치하는 것을 뽑아 사용한다.

#### MessageCodesResolver가 자등으로 생성하는 오류 코드
- FieldError : `rejectValue`
  1. `errorCode.objectName.fieldName`
  2. `errorCode.fieldName`
  3. `errorCode.java.lang.type`
  4. `errorCode`

- ObjectError : `reject`
    1. `errorCode.objectName`
    2. `errorCode`

> 스프링은 검증시, 타입 오류가 발생하면 `typeMismatch`라는 오류 코드를 사용한다.

```java
// 특정 필드 오류 - rejectValue
if (!StringUtils.hasText(member.getNickname())) {
	// required라는 오류코드로 메시지를 찾는다.
	// 1. required.member.nickname
	// 2. required.nickname
	// 3. required.java.lang.String
	// 4. required
	// 위와 같은 순서로 일치하는 메시지를 찾는다.
	bindingResult.rejectValue("nickname", "required");
}

if (!StringUtils.hasText(member.getNickname())) {
	bindingResult.rejectValue("nickname", "required", 
		new Object[]{"arg1", "arg2"}, "default message");
}

// 객체 오류 - reject
if (member.getLoginId().equals(member.getPassword())) {
	// noEqualsIdAndPassword라는 오류코드로 메시지를 찾는다.
	// 1. notEqualsIdAndPassword.member
	// 2. notEqualsIdAndPassword
	// 위와 같은 순서로 일치하는 메시지를 찾는다.
	bindingResult.reject("notEqualsIdAndPassword");
}

if (member.getLoginId().equals(member.getPassword())) {
	bindingResult.reject("notEqaulsIdAndPassword", 
		new Object[]{"arg1, arg2"}, "default message");
}
```

아래는 `messages.properties`의 예시이다. `BindingResult`에 오류 코드를 넘기면 여기서 메시지를 찾아 사용한다.

```properties
#---ObjectError---
#Level1
errorCode.objectName=ErrorMessage and param {0} and {1}.

#Level2
errorCode.objectName=ErrorMessage and param {0}

#----------------------------------------------------------
#---FieldError---
#Level1
errorCode.objectName.fieldName=ErrorMessage

#Level2
errorCode.fieldName=ErrorMessage

#Level3
errorCode.java.lang.String=ErrorMessage
# 스프링은 타입 오류가 발생하면 typeMismatch 라는 오류코드를 사용한다.
typeMismatch.java.lang.Integer=숫자를 입력하세요.

#Level4
errorCode=ErrorMessage
```
> 스프링은 검증시, 타입 오류가 발생하면 `typeMismatch`라는 오류 코드를 사용한다.


## Validator : Interface
컨트롤러에서 `BindingResult`를 사용하여 검증하는 로직을 별도로 분리하여 사용할 수 있다. `Validator` 인터페이스를 구현한 클래스를 만들고, 이를 스프링 빈으로 등록하여 사용하면 된다.

`Validator` 인터페이스의 `supports` 메서드는 구현한 검증기가 어떤 클래스의 객체를 검증할 수 있는지 확인하는 로직을 구현한다.

```java
// 이 검증기는 Member 클래스의 객체를 검증할 수 있다.
@Override
public boolean supports(Class<?> clazz) {
	return Member.class.isAssignableFrom(clazz);
}
```

`Validator` 인터페이스의 `validate` 메서드는 해당 검증기의 로직을 구현한다. 어떤 필드를 검증할 지, 어떤 로직으로 검증할 지를 구현한다. 컨트롤러에서는 `BindingResult` 객체의 `reject`, `rejectValue` 또는 `addError` 메서드를 통해 `FieldError`, `ObjectError`를 직접 생성하여 에러를 추가하다. `Validator`의 `validate` 메서드에서는 `Errors` 파라미터를 통해 `reject`, `rejectValue`, `addError`를 사용할 수 있다.

```java
@Override
public void validate(Object target, Errors errors) {
	Member member = (Member) target;

	if (!StringUtils.hasText(member.getNickname())) {
		errors.rejectValue("nickname", "required", 
			new Object[]{"arg1", "arg2"}, "default message");
	}

	if (member.getLoginId().equals(member.getPassword())) {
		errors.reject("notEqaulsIdAndPassword", 
			new Object[]{"arg1, arg2"}, "default message");
	}
}
```

위와 같이 구현한 검증기는 컨트롤러에서 직접 호출하여 검증하게 할 수도 있고, `WebDataBinder`를 통하여 자동으로 검증하게 할 수도 있다.

- 컨트롤러에서 직접 호출
```java
@Controller
@RequiredArgsConstructor
public class MemberController {

	// 검증기 주입
	private final MemberValidator memberValidator;

	@PostMapping
	public String controllerMethod(
			@ModelAttribute Member member, 
			BindingResult bindingResult) {
		
		// 검증기 동작. 검증에 실패하면 BindingResult에 담아준다.
		memberValidator.validate(member, bindingResult);

		if (bindingResult.hasErrors()) {
			return "오류 발생시 돌려보낼 페이지";
		}

		// 정상 로직.
	}
}
```

- `WebDataBinder`를 통해 검증기 호출과정 생략 가능
```java
@Controller
@RequiredArgsConstructor
public class MemberController {

	// 검증기 주입
	private final MemberValidator memberValidator;

	@InitBinder
	public void init(WebDataBinder dataBinder) {
		// WebDataBinder는 파라미터 바인딩 역할을 해준다. 검증기능도 내부에 포함한다.
		dataBinder.addValidators(memberValidator);
	}

	@PostMapping
	public String controllerMethod(
			// @Validated는 검증기를 실행하라는 애노테이션.
			// WebDataBinder에 등록한 검증기를 찾아서 실행한다.
			@Validated @ModelAttribute Member member, 
			BindingResult bindingResult) {

		if (bindingResult.hasErrors()) {
			return "오류 발생시 돌려보낼 페이지";
		}

		// 정상 로직.
	}
}
```
> `BindingResult`는 검증할 대상 다음에 와야 한다.

> `WebMvcConfigurer`의 `getValidator`를 구현하여 전체 컨트롤러에 해당 검증기를 적용하게 할 수 있다.


## Thymeleaf : BindingResult 사용
타임리프에서는 다음과 같이 `th:errors`, `th:field`를 통해 `BindingResult`에 담긴 정보를 사용할 수 있다.

```html
<div th:if="${#fields.hasGlobalErrors()}">
	<span class="field-error" th:each="err : ${#fields.globalErrors()}">글로벌 오류 메시지</span>
</div>

<div th:field="*{객체의 필드명}" th:errorclass="field-error">
	*   필드에 에러 발생시 `th:errorclass`에 입력한 class 이름을 추가한다.
	*   `th:field`는 정상 상황에서는 모델 객체의 값을 사용한다. 
	**  오류가 발생하면 `FieldError`에서 보관한 값을 사용한다.
</div>
<div class="field-error" th:errors="*{객체의 필드명}">
	*   `th:errors`는 지정한 객체의 필드에 오류가 있으면 출력한다.
</div>
```

## Bean Validation
`Bean Validation`은 애노테이션을 통하여 검증 로직을 편리하게 적용할 수 있도록 공통화하고 표준화 한 것이다. `Bean Validation`은 특정한 구현체가 아닌 Bean Validation 2.0(JSR-380)이라는 기술 표준으로 검증 애노테이션과 여러 인터페이스의 모음을 말한다. 이를 구현한 기술중에 일반적으로 사용하는 구현체는 Hibernate Validator이다.

- Hibernate Validator
  - 공식 사이트: http://hibernate.org/validator/
  - 공식 메뉴얼: https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/ 
  - 검증 애노테이션 모음 : https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/#validator-defineconstraints-spec 

`Bean Validation`을 사용하기 위해서는 `spring-boot-starter-validation` 의존 관계를 추가해야 한다.

```gradle
implementation 'org.springframework.boot:spring-boot-starter-validation'
```

위 의존 관계를 추가하면 스프링 부트는 `LocalValidatorFactoryBean`을 글로벌 Validator로 등록한다. 이 검증기는 `@Validated`와 `@Valid` 애노테이션이 붙은 클래스의 `@NotBlank` 등과 같은 검증 애노테이션을 확인하고 검증을 수행한다. 검증 과정에서 오류가 발생하면 `FiledError`와 `ObjectError`를 생성하여 `BindingResult`에 담는다.

이 때, 검증 필드 오류(`FieldError`)가 발생하면 `MessageCodesResolver`는 애너테이션 이름을 기반으로 오류 코드들을 생성하고, `messages.properties`에서 메시지를 찾아서 사용한다. `MessageCodesResolver`가 오류 코드들을 생성하는 규칙은 [여기](#messagecodesresolver가-자등으로-생성하는-오류-코드)서 확인할 수 있다. 일치하는 메시지가 없다면 애노테이션의 `message` 속성으로 전달된 값을 사용하고, 이 마저 없다면 `validation` 라이브러리가 기본으로 제공하는 값을 사용한다.

`Bean Validation`을 통해 검증할 때, `ObjectError`가 발생하는 경우는 `@ScriptAssert`를 사용하거나 해당 부분만 직접 작성하는 방법을 사용할 수 있다. 하지만 `@ScriptAssert`는 제약이 많고 복잡하며, 검증 기능이 해당 객체의 범위를 넘어서는 경우도 종종 등장하고 대응이 어렵기 때문에 잘 사용하지 않는다. 따라서 `ObjectError` 관련 부분만 코드로 직접 작성하는 것이 좋다.

#### 검증 대상 선택
또한 `Bean Validation`은 `groups` 기능을 통해 검증 대상의 특정 필드를 선택하여 검증할 수 있도록 지원한다. 방법은 다음과 같다.

- `SaveCheck`, `UpdateCheck` 등과 같은 빈 인터페이스를 만든다.
- 이를 BeanValidation 애노테이션에 `(groups = {SaveCheck.class, UpdateCheck.class})`와 같이 적용할 그룹을 속성으로 넘겨준다.
- Controller에서 `@Validated(SaveCheck.class)`와 같이 어떤 그룹에 검증을 진행할 지 선택한다.

하지만 `groups` 기능은 컨트롤러로 전달되는 데이터와 이를 바인딩받는 객체가 일치하지 않기 때문에 잘 사용하지 않는다. 따라서 해당 기능을 이용하기보다는 데이터를 주고받는 DTO 객체를 따로 만들어서 여기에 `Bean Validation`을 적용하고, 검증에 성공하면 이를 `Entity` 등으로 변환하여 사용하는 것이 더 좋은 선택이다.

## API 검증
`@Valid`와 `@Validated`는 `@RequestBody`에도 적용할 수 있다. `@RequestBody`는 `HttpMessageConverter`를 통하여 JSON 데이터를 객체로 바인딩해주는 역할을 한다.

```java
@PostMapping
public Object contollerMethod(
	@RequestBody @Validated MemberSaveRequestDto requestDto,
	BindingResult bindingResult) { ... }
```

`HttpMessageConveret`가 JSON 데이터를 객체로 바인딩에 성공하여 컨트롤러로 넘어오면, `Validator`가 동작하여 객체를 검증한다. 검증에 실패하게 되면 API 응답으로 검증에 실패하여 로직을 수행하지 못하였다는 사실을 알려야 한다. `BindingResult`에는 검증 실패에 대한 모든 정보가 담겨있다. 이를 그대로 반환하는 것은 너무 과하므로, 검증에 실패하면 `BindingResult`에서 필요한 데이터만 선택하여 API 스펙에 맞게 반환하도록 하는 것이 좋다.

> `HttpMessageConverter`가 JSON을 객체로 바인딩 할 때, 타입 오류 때문에 객체에 바인딩하는 것 자체가 실패하면 `@Validated`가 동작하지 않는다.
> 
> `@ModelAttribute`는 필드 단위로 정교하게 바인딩이 적용되기 때문에 특정 필드가 바인딩 되지 않아도 나머지 필드는 정상적으로 바인딩 된다. 따라서 `Validator`를 사용한 검증도 적용이 가능하다.
> 
> 반면 `@RequestBody`는 `HttpMessageConverter`가 동작하여 JSON 데이터를 객체 필드에 바인딩하는 중에 타입 오류로 인하여 바인딩하지 못하면 해당 단계에서 `HttpMessageNotReadableException` 예외가 발생하고, 더 이상 진행하지 않는다. 따라서 컨트롤러도 호출되지 않고 `Validator`도 적용할 수 없다. 이 경우, 예외 처리를 통해 예외 API 응답을 내려주도록 해야 한다.