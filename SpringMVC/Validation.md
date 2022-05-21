# Validation
컨트롤러의 역할은 HTTP 요청이 정상인지 검증하는 것이다. 따라서 검증 로직을 잘 개발해야한다.

HTTP 요청은 클라이언트에서 검증할 수 있고 서버에서도 검증할 수 있다. 클라이언트 검증은 자바스크립트를 통해 프론트 단에서 요청을 보내기 전에 검증하는 것이고 서버 검증은 자바 스프링 등을 통해 서버에서 전송받은 요청을 백 단에서 검증한다.
클라이언트 검증은 조작할 수 있기 때문에 보안에 취약하다. 서버만으로 검증하게 되면 즉각적인 고객 사용성이 부족해진다. 따라서 이 둘을 적절히 잘 섞어서 사용해야 하며 최종적으로 서버 검증은 필수이다. API 방식을 사용하면 API 스펙을 잘 정의하여 검증 오류를 API 응답 결과에 잘 남겨주도록 한다.

- `BindingResult` 객체는 스프링이 제공하는 검증 오류를 보관하는 객체로 검증 오류가 발생하면 여기에 보관한다. 이게 있으면 `@ModelAttribute`에 데이터 바인딩 시 오류가 발생해도 `BindingResult`에 오류정보를 담아서 컨트롤러를 정상적으로 호출한다.
- `BindingResult`에 검증 오류를 적용하는 방법은 3가지가 있다.
	1. `@ModelAttribute`의 객체에 타입오류 등으로 바인딩이 실패하면 스프링이 `FieldError`를 생성해서 넣어준다.
	2. 개발자가 직접 넣어주는 방법
	3. `Validator`를 사용하는 방법

아래 코드들은 1, 2번에 해당한다. 
`src/main/resources/errors.properties`
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
# 스프링은 타입 오류가 발생하면 typeMismatch 라는 오류코드를 사용
typeMismatch.java.lang.Integer=숫자를 입력하세요.

#Level4
errorCode=ErrorMessage
```
- 오류 메시지 파일. `BindingResult`에서 메시지 코드를 넘기면 여기서 찾아 사용한다.

`controller`
```java

private final ItemValidator itemValidator;

@InitBinder
public void init(WebDataBinder dataBinder) {
	// 검증기 자동으로 적용.
	dataBinder.addValidators(itemValidator);
}

@PostMapping // @Validated @Valid 둘다 사용 가능.
public String controllerMethod(@Validated @ModelAttribute Item item, BindingResult bindingResult, RedirectAttributes redirectAttributes) {

	// 검증
	// itemValidator.validate(item, bindingResult);
	// WebDataBinder에 검증기를 추가하면 해당 컨트롤러에서는 검증기를 자동으로 적용 가능. 글로벌 설정은 별도.

	// 에러 존재하면 에러 메시지와 함께 현재 페이지로 다시 보낸다.
	if (bindingResult.hasErrors()) {
		return "보낼 위치";
	}

	// 성공 로직
	// ...
}
```

`ObjectValidator`
```java
@Component // 스프링 빈으로 등록.
public class ItemValidator implements Validator {
	
	// 해당 검증기를 지원하는지 여부 확인.
	@Override
	public boolean supports(Class<?> clazz) {
		return 검증대상클래스.class.isAssignableFrom(clazz);
	}
	
	// 검증. 파라미터로 검증 대상 객체와 BindingResult를 받는다.
	@Override
	public void validate(Object target, Errors errors) {
		검증할객체클래스 objectName = (검증할객체클래스) target;

		// 특정 필드 예외.
		ValidationUtils.rejectIfEmptyOrWhitespace(errors, "itemName", "errorCode"); // empty와 공백 같은 단순한 기능만 제공한다.
		
		// 위의 코드를 풀면 다음과 같다.
		if (!StringUtils.hasText(item.getItemName())) {
			// errors.addError(new FieldError("objectName", "fieldName", item.getName(), false, new String[]{"xxx.objectName.fieldName"}, new Object[]{123, 1234},  "defaultMessage"));
			// new FieldError(objectName, field, rejectedValue, bindingFailure, codes, arguments, defaultMessage)
			// 파라미터 설명(오류발생 객체명, 오류필드, 사용자가 입력한 값-다시 페이지에 띄워줄거, 바인딩실패(타입오류 등)여부, 메시지 코드, 메시지에서 사용하는 인자, 기본 오류 메시지)
		
			errors("fieldName", "xxx", new Object[]{123, 1234}, "defaultMessage");
			// 위와 동일하게 동작하는 코드
			// errors.rejectValue(오류필드명 ,messageResolver를 위한 오류 코드, 오류 메시지에서 사용하는 인자, 기본 오류 메시지);
		}

		// 전체 예외.
		if (조건) {
			// errors.addError(new ObjectError("item", null, null ,"defaultMessage"));
			errors.reject("xxxx", new Object[]{12345}, "defaultMessage");
			// 위와 동일하게 동작하는 코드
			// errors.reject(messageResolver를 위한 오류 코드, 오류 메시지에서 사용하는 인자, 기본 오류 메시지)
		}
	}
}
```
- `FieldError`를 직접 다루는 방법
	- 특정 필드에 오류가 있으면 `FieldError` 객체를 생성하여 bindingResult에 담는다.
	- 특정 필드를 넘어서는 오류는 `ObjectError` 객체를 생성하여 bindingResult에 담는다.
	- 메시지 코드는 하나가 아니라 배열로 여러 값을 전달할 수 있는데, 순서대로 매칭해서 처음 매칭되는 메시지를 사용한다.
- `BindingResult.rejectValue`를 통해 오류 코드를 다루는 방법🌟
	- `BindingResult`는 어떤 객체를 대상으로 검증하는지 target을 이미 알고 있기 때문에 필드명 만으로도 오류 메시지를 넣어줄 수 있다.
	- `MessageCodesResolver`를 통해 오류 메시지를 다룬다.
	- `MessageCodesResolver`는 검증 오류 코드로 메시지 코드들을 생성한다. 인터페이스이기 때문에 구현체가 필요 -> 기본 구현체는 `DefaultMessageCodesResolver`
	- **기본 메시지 생성 규칙**은 아래로..

`thymeleaf`
```html
...
<div th:if="${#fields.hasGlobalErrors()}">
	<span class="field-error" th:each="err : ${#fields.globalErrors()}">글로벌 오류 메시지</span>
</div>

<div th:field="*{객체의 필드명}" th:errorclass="field-error">
	필드에 에러 발생시 errorclass에 입력한 class이름을 추가한다.
	th:field는 정상 상황에서는 모델 객체의 값을 사용. 오류가 발생하면 FieldError에서 보관한 값을 사용한다.
</div>
<div class="field-error" th:errors="*{객체의 필드명}">
	지정한 객체의 필드에 오류가 있으면 출력
</div>
...
```
- 타임리프에서 에러를 위와 같이 처리할 수 있다.


### DefaulteMessageCodesResolver의 기본 메시지 생성 규칙

객체 오류의 경우 다음 순서로 2가지를 생성한다
> 1 -> code + “.” + objectName  
> 2 -> code  

필드 오류의 경우 다음 순서로 4가지 메시지 코드 생성한다
> 1 -> code.objectName.fieldName  
> 2 -> code.fieldName  
> 3 -> code.fieldType  
> 4 -> code  



- - - -
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


#Validation
#Validation/errorMessage
#Validation/BindingResult
#Validation/BeanValidation
- - - -
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.