# Validation
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

`BindingResult`의 `rejectValue`, `reject` 메서드를 사용하면 `FieldError`와 `ObjectError`를 직접 생성하지 않고도 검증 오류를 담을 수 있다. 
`reject`와 `rejectValue` 메서드는 `errorCode`를 인자로 받는다. 여기서 `errorCode`는 `messages.properties`에 등록된 코드가 아니라 `messageResolver`를 위한 오류 코드이다. 내부에서 `FieldError`, `ObejctError`를 생성하고, `messageResolver`가 자동으로 오류 코드들을 생성한다. 다음과 같은 규칙으로 오류 코드를 자동으로 생성하고, `messages.properties`에서 순위에 따라 일치하는 것을 뽑아 사용한다.

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



---
## Bean Validation
- 공식 사이트: http://hibernate.org/validator/
- 공식 메뉴얼: https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/ 
- 검증 애노테이션 모음 : https://docs.jboss.org/hibernate/validator/6.2/reference/en-US/html_single/#validator-defineconstraints-spec 

`Bean Validation`은 검증 로직을 모든 프로젝트에 적용할 수 있도록 공통화, 표준화 한 것. 애노테이션 하나로 검증 로직을 매우 편리하게 적용할 수 있다.
`Bean Validation`은 특정한 구현체가 아닌 Bean Validation 2.0(JSR-380)이라는 기술 표준으로 검증 애노테이션과 여러 인터페이스의 모음이다. 이를 구현한 기술중에 일반적으로 사용하는 구현체는 하이버네이트 Validator이다.

이를 사용하기 위해서는 의존관계 추가 필요
```
implementation ‘org.springframework.boot:spring-boot-starter-validation
```
`jakarta.validation-api` : Bean Validation 인터페이스
`hibernate-validator` : 구현체

### 필드에러
다음과 같은 애노테이션을 검증 대상 필드에 붙임으로써 검증을 수행할 수 있다.
```java
@NotBlank
@NotNull
@Range(min = 100, max = 10000)
@Max(9999)
```

스프링 부트가 `spring-boot-starter-validation`라이브러리를 넣으면 자동으로 Bean Validator를 인지하고 스프링에 통합한다. 따라서 스프링 MVC는 Bean Validator를 사용할 수 있다. 스프링 부트는 자동으로 `LocalValidatorFactoryBean`을 글로벌 Validator로 등록한다. 이는 `@NotNull`과 같은 애노테이션을 보고 검증을 수행한다. 검증 오류가 발생하면 이 Validator가 `FieldError`와 `ObjectError`를 생성해서 `BindingResult`에 담아주는 것이다.
이 때, 검증 순서는 다음과 같다.
1. `@ModelAttribute` 각각의 필드에 타입 변환을 시도하고
2. 성공하면 Validator를 적용한다.
3. 실패하면 `typeMismatch`로 `FieldError`를 추가한다. -> 이 때, 바인딩에 실패한 필드는 BeanValidation을 적용하지 않는다.

Bean Validation을 적용하면 오류 코드가 애노테이션 이름으로 등록된다. 따라서 `errors.properties`에 다음과 같이 메시지를 등록하면 오류 메시지를 적용할 수 있다.
```properties
# 애노테이션이름.대상객체명.필드명=오류메시지
# 애노테이션이름.필드명=오류메시지
# 애노테이션이름.java.lang.String=오류메시지
# 애노테이션이름
# {0}은 필드명, {1}, {2} 등은 애노테이션마다 다르다.

NotBlank.item.itemName={0}, 상품 이름을 입력하세요. 
NotBlank.itemName=이름을 입력하세요.
Range.java.lang.Integer=...
Range={2} ~ {1}
```
또는 애노테이션에서 message 속성을 사용하여 오류 메시지를 입력한다.
```java
@NotBlank(message = "공백 허용 안함")
private String itemName;
```

Bean Validation이 메시지를 찾는 순서는
1. 생성된 메시지 코드 순서대로 messageSource에서 찾는다.
2. 애노테이션의 `message` 속성을 사용한다.
3. 라이브러리의 기본 제공값을 사용한다.

### 오브젝트 에러
`@ScriptAssert()`가 있는데 이는 제약이 많고 복잡하고, 검증 기능이 해당 객체의 범위를 넘어서는 경우도 종종 등장하고 대응이 어렵기 때문에 잘 사용하지 않는다.
따라서 오브젝트 오류 관련 부분만 코드로 직접 작성하는 것이 낫다. -> 컨트롤러가 아니라 따로 빼서 관리하면 좋을 듯 하다.


### 적용
Bean Validation을 Entity에 적용하면 Form 또는 Dto에 대해 등록, 수정 과정에 대해 나누어 검증할 수 없다. 두 상황 모두에 Bean Validation이 동작하기 때문이다. 이를 해결하기 위한 방법은 두가지가 있다.
- BeanValidation의 groups 기능을 사용.
	- `SaveCheck`, `UpdateCheck` 등과 같은 빈 인터페이스를 만든다.
	- 이를 BeanValidation 애노테이션에 `(groups = {SaveCheck.class, UpdateCheck.class})`와 같이 적용할 그룹을 속성으로 넘겨준다.
	- Controller에서 `@Validated(SaveCheck.class)`처럼 그룹을 적용한다.
- 객체를 직접 사용하지 않고 SaveForm, UpdateForm 등 Form, Dto 전송을 위한 별도의 모델 객체를 만들어 사용한다.
	- 전송을 위한 Form or Dto를 만들고 여기에 BeanValidation 애노테이션을 적용
	- Controller에서 Entity 객체가 아닌 BeanValidation을 적용한 전송용 객체 바인딩
		- `@ModelAttribute("이름")`을 적용하여 모델에 넣을 때, 이름 지정 가능
	- 해당 객체를 Entity 객체로 변환하여 작업 수행.

-> 별도의 모델 객체를 만들어 사용하고 여기에 검증을 하는 것이 좋다. 전송하는 폼 데이터가 복잡해도 이에 맞춘 별도의 폼 객체를 사용해서 데이터를 전달을 수 있다. 검증이 중복되지 않는다. 

Bean Validation을 이용하면 `Validator`를 구현한 `ObjectValidator`를 할 필요가 없다 -> 오류 검증기가 중복 적용된다.
```java
// 아래 코드가 있다면 제거
private final ItemValidator itemValidator;

@InitBinder
public void init(WebDataBinder dataBinder) {
	dataBinder.addValidators(itemValidator);
}
```



### API 방식
`@RequestBody`에도 `@Validated` 적용 가능하다.
```java
@PostMapping
public Object method(@RequestBody @Validated ItemSaveDto itemSaveDto, BindingResult bindingResult) {
	...
}
```

API 경우 3가지 경우를 나누어 생각해야 한다.
- 성공 요청 : 성공
- 실패 요청 : JSON을 객체로 생성하는 것 자체가 실패(타입오류 등) -> 컨트롤러 자체가 호출되지 않는다. 검증 불가능. 검증은 컨트롤러가 호출 되야 수행된다.
- 검증 오류 요청 : JSON을 객체로 생성하는 것은 성공, 검증 실패

- `@ModelAttribute`는 필드 단위로 정교하게 바인딩이 적용된다. 특정 필드가 바인딩 되지 않아도 나머지 필드는 정상 바인딩 되고, Validator를 사용한 검증도 적용할 수 있다. 
- `@RequestBody`는 HttpMessageConverter 단계에서 JSON 데이터를 객체로 변경하지 못하면 이후 단계 자체가 진행되지 않고 예외가 발생한다. 컨트롤러도 호출되지 않고, Validator도 적용할 수 없다. 

`HttpMessageConverter` 단계에서 실패하면 예외가 발생한다. -> 예외 처리 필요

