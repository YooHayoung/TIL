# ArgumentResolver

`ArgumentResolver`는 `org.springframework.web.method.support.HandlerMethodArgumentResolver`를 말한다. 

이 `ArgumentResolver`는 컨트롤러가 필요로하는 다양한 파라미터의 값을 생성하는 역할을 한다. 값이 모두 생성되면, 컨트롤러를 호출하면서 생성한 값을 넘겨준다.

스프링은 30개가 넘는 `ArgumentResolver`를 기본으로 제공하여 `HttpServletRequest`, `Model`, `@RequestParam`, `@ModelAttribute`, `HttpEntity` 등, 여러 파라미터를 유연하게 처리할 수 있도록 해준다. 

`ArgumentResolver`의 동작 방식은 다음과 같다.

1. `supportsParameter` 메서드를 호출하여 해당 파라미터를 지원하는지 확인한다.
2. 해당 파라미터를 지원한다면 `resolveArgument` 메서드를 호출한다. `resolveArgument` 메서드는 실제 객체를 생성하여 반환하는 작업을 한다. 반환된 객체는 컨트롤러 호출시 넘어가게 된다.


`ArgumentResolver`는 `HandlerMethodArgumentResolver` 인터페이스를 구현하고, 구현체를 `WebMvcConfigurer`에 등록하면 된다. 아래는 `QueryStringArg`라는 애노테이션을 만들고, 쿼리스트링의 값을 해당 애노테이션이 붙은 파라미터에 바인딩하기 위해 `ArgumentResolver`를 구현하고, 이를 등록하는 과정이다.

`ArgumentResolver`를 적용시키기 위한 애노테이션을 만든다. 컨트롤러의 파라미터에서 해당 애노테이션이 붙은 객체는 `ArgumentResolver`가 동작하여 값을 바인딩 받도록 한다.

```java
// 파라미터에만 적용한다.
@Target(ElementType.PARAMETER)
// 리플렉션 등을 활용할 수 있도록 런타임까지 애노테이션 정보가 남아있다.
@Retention(RetentionPolicy.RUNTIME) 
public @interface QueryStringArg {
}
```

다음으로 `HandlerMethodArgumentResolver`를 구현한다. 
`supportsParameter`를 구현하여 컨트롤러의 어떤 파라미터에 현재 구현하는 `ArgumentResolver`를 적용할 지 체크하도록 한다.
다음으로 `resolveArgument`를 구현하여 파라미터에 어떤 값을 생성하여 넘겨줄지 구현한다.

- 아래에서 사용한 `ObjectMapper`는 Json <-> Java Object, Java List, Java Map, Jackson JsonNode 등으로 직렬화, 역직렬화 등이 가능한 클래스이다. `ObjectMapper`의 `readValue` 메서드를 이용하면 Json 문자열을 통해 지정한 자바 객체에 값을 채워 생성할 수 있다.

```java
public class QueryStringArgumentResolver implements HandlerMethodArgumentResolver {

    private final ObjectMapper mapper;

    public QueryStringArgumentResolver(ObjectMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        // getParameterAnnotation을 통해 파라미터에 붙은 @QueryStringArg 애노테이션을 가져온다.
        // 파라미터에 해당 애노테이션이 붙어있지 않으면 null을 반환한다.
        // 파라미터마다 이를 수행하여 확인한다.
        return parameter.getParameterAnnotation(QueryStringArg.class) != null;
    }

    @Override
    public Object resolveArgument(MethodParameter parameter,
                                  ModelAndViewContainer mavContainer,
                                  NativeWebRequest webRequest,
                                  WebDataBinderFactory binderFactory) throws Exception {

        HttpServletRequest request = (HttpServletRequest) webRequest.getNativeRequest();
        // 요청에서 쿼리스트링 부분을 뽑아낸다.
        String queryString = request.getQueryString();

        // 쿼리스트링이 존재하지 않으면, 비어있으면 ObjectMapper에 빈 Json을 반환한다.
        // 빈 Json을 반환하면 필드 값이 null인 객체를 생성하여 파라미터에 담아준다.
        if (StringUtils.isEmpty(queryString)) {
            return mapper.readValue("{}", parameter.getParameterType());
        }
        // 쿼리스트링을 Json 문자열 형태로 변환한다.
        String json = queryStringToJson(queryString);

        // Json 문자열 형태의 쿼리스트링을 ObjectMapper에 넘겨주어 값을 바인딩하고, 이를 반환한다.
        return mapper.readValue(json, parameter.getParameterType());
    }

    private String queryStringToJson(String queryString) throws UnsupportedEncodingException {
        String jsonPrefix = "{\"";
        String jsonSuffix = "\"}";

        // 쿼리스트링을 받으면 UTF-8 형태로 인코딩 되어있다.
        // 이를 그대로 쓰면 한글의 경우, 인코딩 된 문자열을 사용하게 된다.
        // 쿼리스트링을 디코딩하여 한글을 복원해준다.
        String result = URLDecoder.decode(queryString, StandardCharsets.UTF_8)
                .replaceAll("=", "\":\"")
                .replaceAll("&", "\",\"");

        return jsonPrefix + result + jsonSuffix;
    }
}
```

`HandlerMethodArgumentResolver` 구현을 완료하였다면 이를 `WebMvcConfigurer`에 등록해야 한다. `WebMvcConfigurer` 인터페이스의 `addArgumentResolvers`를 구현하여 구현한 `ArgumentResolver`를 등록한다.

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
        resolvers.add(new QueryStringArgumentResolver());
    }
}
```

이제 컨트롤러에서 파라미터에 `@QueryStringArg` 애노테이션이 붙어있다면 구현 및 등록한 `ArgumentResolver`가 동작하여 값을 매핑해준다.

```java
@RestController
public class Controller {
    @GetMapping
    public ResponseEntity<?> getExample(
        @QueryStringArg ItemSearchCond searchCond) { ... }
}
```
