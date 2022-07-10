# API 예외 처리
API의 경우, 각 오류 상황에 맞는 오류 응답 스펙을 정하고, JSON으로 데이터를 내려줘야 한다.

`WebServerFactoryCustomizer`를 구현한 클래스를 통해 서블릿에 오류페이지를 등록한 후 에러 페이지 컨트롤러에서 API 응답을 내려주도록 해야한다. API로 내려주도록 지정해주지 않으면 기존 등록한대로  HTML이 반환 될 것이다. 다음과 같은 방식으로 컨트롤러를 작성하면 된다.
```java
@RequestMapping(value = "오류페이지경로", produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Map<String, Object>> errorPageApi(HttpServletRequest request, HttpServletResponse response) {

	// ResponseEntity에 Map으로 키, 값 쌍으로 데이터를 넣고 request에서 상태코드 꺼내서 사용.

}
```

스프링 부트는 이를 편리하게 이용할 수 있도록 기능을 제공한다.

## 스프링 부트 기본 오류 처리
스프링 부트에서 제공하는 기본 오류 처리 컨트롤러인 `BasicErrorController`는 에러 페이지를 처리하는 두 개의 메서드가 있는데 하나는 클라이언트 요청의 Accept 헤더 값이 `text/html`인 경우에 호출하여 view를 제공하는 `errorHtml()` 메서드, 또 다른 하나는 그 외의 경우에 호출되어 `ResponseEntity`로 반환하는 `error()` 메서드가 있다. 스프링 부트는 `BasicErrorController`가 제공하는 기본 정보들을 활용하여 오류 API를 생성해준다.


## HandlerExceptionResolver : ExceptionResolver
스프링 MVC는 핸들러 밖으로 예외가 던져진 경우, 예외를 해결하고 동작을 새로 정의할 수 있는 방법을 제공한다. 핸들러 밖으로 던져진 예외를 해결하고, 동작 방식을 변경하고 싶으면 `HandlerExceptionResolver`를 사용하면 된다.

`ExceptionResolver`를 적용하게 되면 WAS로 바로 예외가 전달되는 것이 아니라 핸들러에서 전달된 예외를 `ExceptionResolver`에서 일단 예외 해결을 시도한다. 예외를 처리하면 정상응답 처리가 된다. 예외를 처리하지 못하면 그 때 WAS로 예외가 호출된다. 참고로 `ExceptionResolver`로 예외를 해결해도 인터셉터의 `postHandle()`은 호출되지 않는다.

### 적용 방법
`HandlerExceptionResolver` 인터페이스의 `resolveException()` 메서드를 구현하고 `WebMvcConfigurer`를 통해 등록한다.
```java
// 구현
public class ExampleExceptionResolver implements HandlerExceptionResolver {

	private final ObjectMapper objectMapper = new ObjectMapper();

	@Override
	public ModelAndView resolveException(...) {
		try {
			// 원하는 오류 타입이면 처리.
			if (ex instanceof IllegalArgumentException) {
				// 상태 코드를 지정하고 메시지를 담는다.
				// response.sendError(HttpServletResponse.SC_BAD_REQUEST, ex.getMessage());

				// response.getWriter().println("내용"); 을 통해 응답 바디에 직접 데이터를 넣어주는 것도 가능.

				// Exception을 처리해서 정상 흐름처럼 변경한다.
				// 빈 ModelAndView를 반환하면 뷰를 렌더링 하지 않고 정상 흐름으로 서블릿 리턴.
				// View, Model 등의 정보를 지정해서 반환하면 뷰를 렌더링.
				// return new ModelAndView();


				/////////////////////////////////////
				// 응용. 요청 헤더의 accept 값이 json이면 JSON, 그 외에는 HTML 처리.
				String acceptHeader = request.getHeader("accept");
				response.setStatus(HttpServletResponse.SC_BAD_REQUEST);

				if ("application/json".eqauls(acceptHeader)) {
					Map<String, Object> errorResult = new HashMap<>();
					// errorResult에 데이터 담아서.
					String result = objectMapper.writeValueAsString(errorResult);

					reponse.setContentType("application/json");
					reponse.setCharacterEncoding("utf-8");
					reponse.getWriter().write(result);
					return new ModelAndView();
				} else {
					return new ModelAndView("error/pageName");
				}
			}
		} catch (IOException e) {
			log.error("e = ", e);
		}

		return null;
		// null을 반환하면 다음 ExceptionResolver를 찾아서 실행.
		// 없으면 예외 처리가 실패하고 기존에 발생한 예외를 서블릿 밖으로 던진다.
	}
}

// 등록
@Configuration
public class WebConfig implements WebMvcConfigurer {

	@Override
	public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver resolvers) {
		resolvers.add(new ExampleExceptionResolver());
	}
}
```
	- `configureHandlerExceptionResolvers(..)` 을 사용하면 스프링이 기본으로 등록하는 `ExceptionResolver`가 제거되기 때문에 주의해야 한다.
	- 예외를 처리하여 정상 동작하도록 하기 때문에 `ExceptionResolver`에서 상태 코드를 변경해주지 않으면 상태코드가 200 ok로 전송된다. 조심하자.




## 스프링이 제공하는 ExceptionResolver
직접 `ExceptionResolver`를 구현하는 것은 복잡하다. 스프링에는 이를 편리하게 사용할 수 있도록 기본으로 제공하는 `ExceptionResolver`들이 있다. `HandlerExceptionResolverComposite`에 다음과 같은 순서로 등록이 되어있다.

1. `ExceptionHandlerExceptionResolver`
	- `@ExceptionHandler`를 처리한다. API 예외처리는 대부분 이를 사용한다. 마지막에 설명.
2. `ResponseStatusExceptionResolver`
	- HTTP 상태 코드를 지정해준다.
	- `@ResponseStatus` 애노테이션이 붙은 예외, `ResponseStatusException`로 발생한 예외를 처리한다.
3. `DefaultHandlerExceptionResolver`
	- 스프링 내부 기본 예외를 처리한다.


### ResponseStatusExceptionResolver
예외에 `@ResponseStatus` 애노테이션을 적용하면 **HTTP 상태코드를 변경**해준다.
```java
// Http 상태 코드를 400으로 변경하고 메시지에 "에러 메시지"를 담아서 전송.
// reason은 MessageSource에서 찾는 기능도 있다. reason = "error.bad"
@ResponseStatus(code = HttpStatus.BAD_REQUEST, reason = "에러 메시지")
public class UserDefineException extends RuntimeException {}
```

`@ResponseStatus`은 개발자가 직접 변경할 수 없는 예외에는 적용할 수 없다. 또한, 애노테이션이기 때문에 조건에 따라 동적으로 변경하기 힘들다. 이를 위해 `ResponseStatusException` 예외를 사용하면 된다.
```java
@GetMapping
public String exampleControllerMethod() {
	throw new ResponseStatusException(HttpStatus.NOT_FOUND, "에러 메시지", new RunTimeException());
}
```
상황에 따라 동적으로 변경 가능하다.

### DefaultHandlerExceptionResolver
`DefaultHandlerExceptionResolver`는 스프링 내부 예외 처리에 사용된다. 
대표적으로 파라미터 바인딩 시점에 타입이 맞지 않으면 `TypeMismatchException`이 발생하는데 이를 그냥 두면 서블릿 컨테이너까지 오류가 올라가고 500 오류가 발생한다. 하지만 대부분 파라미터 바인딩은 클라이언트가 HTTP 요청 정보를 잘못 호출해서 발생하는 문제이기 때문에 HTTP는 이런 경우 상태 코드 400을 사용하도록 되어있다.
`DefaultHandlerExceptionResolver`는 이러한 경우에 500 오류가 아닌 400 오류로 변경한다.

`DefaultHandlerExceptionResolver.handleTypeMismatch`를 확인해보면 `response.sendError()`를 통해서 문제를 해결하는 것을 볼 수 있다. `BasicErrorController`의 `error()` 메서드를 사용하는 것으로 볼 수 있다. 따라서 WAS에서 다시 오류 페이지를 요청하게 된다.


## ExceptionHandlerExceptionResolver 
`HandlerExceptionResolver`를 직접 사용하는 것은 복잡하다. API 오류 응답은 `response`에 직접 데이터를 넣어주어야 하기 때문에 매우 불편하고, `ModelAndView`를 반환하는 것도 잘 맞지 않는다. 이를 해결하기 위해 스프링은 `ExceptionHandlerExceptionResolver`를 제공한다.

### @ExceptionHandler & @ControllerAdvice
`ExceptionHandlerExceptionResolver`는 `@ExceptionHandler` 애노테이션을 사용하는 예외 처리 기능이다.
	- `@ExceptionHandler` 애노테이션을 선언하고 처리하고 싶은 예외를 지정하여 사용한다. 지정한 예외 또는 그 예외의 자식 클래스는 모두 잡을 수 있다.
	- `@ExceptionHandler({ExceptionA.class, ExceptionB.class})` 처럼 여러 예외를 한번에 잡을 수 있다.
	- `@ExceptionHandler`에 예외를 생략하면 메서드 파라미터의 예외가 지정된다.
	- 파라미터와 응답 지정은 공식 메뉴얼 참조
		- https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-ann-exceptionhandler-args 

`@ControllerAdvice`는 대상으로 지정한 여러 컨트롤러에 `@ExceptionHandler`, `@InitBinder` 기능을 부여해준다. 대상을 지정하지 않으면 모든 컨트롤러에 적용된다.
`@RestControllerAdvice`는 `@ControllerAdvice`에 `@ResponseBody`가 추가된 것이다.
	- `@ControllerAdvice`의 대상 컨트롤러 지정의 자세한 방법은 스프링 공식 문서 참고
		- https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#mvc-ann-controller-advice 

사용하는 방법은 다음과 같다.
```java
// @ControllerAdvice, @RestControllerAdvice를 사용하여 컨트롤러와 예외처리 코드를 분리한다.

// @ControllerAdvice(annotations = RestController.class)
// @ControllerAdvice("패키지경로")
@RestControllerAdvice(assignableTypes = {ControllerInterface.class, AbstractController.class})
public class ExampleControllerAdvice {
	// @ExceptionHandler 애노테이션을 사용하여 처리할 예외를 지정한다.

	// 방법 1. 상태코드 지정, 처리할 예외 지정
	// ErrorResult는 예외 발생시 API 응답 객체이다.
	@ResponseStatus(HttpStatus.BAD_REQUEST)
	@ExceptionHandler(IllegalArgumentException.class)
	public ErrorResult method1(IllegaArgumentException e) {
		return new ErrorResult("...", e.getMessage());
	}

	// 방법 2. ResponseEntity 객체 이용. @ExceptionHandler에 예외를 생략하면 메서드 파라미터의 예외가 지정된다.
	@ExceptionHandler
	public ResponseEntity<ErrorResult> method2(RunTimeException e) {
		ErrorResult errorResult = new ErrorResult("...", e.getMessage());
		return new ResponseEntity<>(errorResult, 상태코드);
	}

	// 방법 3. 1, 2에서 놓친 모든 에러는 여기서 처리하도록 한다.
	@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
	@ExceptionHandler
	public ErrorResult method3(Exception e) {}

	// 방법 4. 응답값을 ModelAndView로 하여 HTML을 응답으로 사용할 수 있다.
	@ExceptionHandler(ExceptionKK.class)
	public ModelAndView method4(ExceptionKK e) {
		return new ModelAndView("에러 페이지");
	}
}
```







#스프링 MVC/API 예외 처리#
- - - -
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.