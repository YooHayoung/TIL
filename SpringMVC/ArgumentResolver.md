# ArgumentResolver
#내용 추가 필요#
ArgumentResolver 설명…


특정 애노테이션을 만들고 해당 애노테이션이 있으면 직접 만든 `ArgumentResolver`가 동작해서 기능을 수행하도록 하면 개발 생산성이 증가될 것이다.
예를 들어, `@SessionAttribute(name="세션이름", required=false)`와 같은 기능을 하는 `@Login` 이라는 애노테이션을 만들고 이를 계속해서 사용하도록 하려면 다음과 같은 과정을 거친다.

`Controller`
```java
@GetMapping
public String sessionAttributeExamp(
	// @SessionAttribute(name="세션이름", required=false) Member loginM) {
	@Login Member loginM {
	// @Login 애노테이션은 직접 정의한 애노테이션으로 위의 @SessionAttribute와 같은 기능을 하도록 한다.

	// ...로직
}
```

`@Login Annotation`
```java
@Target(ElementType.PARAMETER) // 파라미터에만 적용한다.
@Retention(RetentionPolicy.RUNTIME) // 리플렉션 등을 활용할 수 있도록 런타임까지 애노테이션 정보가 남아있다.
public @interface Login {
}
```

`HandlerMethodArgumentResolver` 구현
```java
public class TestArgumentResolver implements HandlerMethodArgumentResolver {

    @Override
    public boolean supportsParameter(MethodParameter parameter) {

		  // 파라미터가 (컨트롤러에서 애노테이션이 붙은 파라미터)
		  // parameter.hasParameterAnnotation(애노테이션명.class) 애노테이션이 있으면서 
		  // 클래스지정.class.isAssignableFrom(parameter.getParameterType()) 지정한 클래스와 파라미터의 클래스 타입이 같으면 이 ArgumentResolver가 사용된다.
        boolean hasLoginAnnotation = parameter.hasParameterAnnotation(Login.class);
        boolean hasMemberType = Member.class.isAssignableFrom(parameter.getParameterType());

        return hasLoginAnnotation && hasMemberType;
    }

	  // 컨트롤러 호출 직전에 호출되어서 필요한 파라미터 정보를 생성해준다.
    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {
		  // 해당 애노테이션에서 필요한 로직을 수행하면 된다.
		
        HttpServletRequest request = (HttpServletRequest) webRequest.getNativeRequest();
        HttpSession session = request.getSession(false);
        if (session == null) {
            return null;
        }

		  // session에 저장된 로그인된 Member 객체 반환.
        return session.getAttribute(SessionConst.LOGIN_MEMBER);
    }
}

```


`WebConfig`에 구현한 `ArgumentResolver`를 등록해준다.
```java
@Override
public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
    resolvers.add(new TestArgumentResolver());
}
```



- - - -
해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.