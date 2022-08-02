# Spring Security

## Authentication Architecture
<img src="https://user-images.githubusercontent.com/81250857/182189122-393e7419-1529-45b3-aaf7-1a9b06195c0b.png">

### AuthenticationFilter
`AuthenticationFilter`는 설정된 로그인 URL로 오는 요청을 감시하고, `user` 인증을 처리한다.

스프링 시큐리티는 접근 권한이 없는 경우, 기본적으로 `UsernamePasswordAuthenticationFilter`를 사용한다. 로그인 요청이 오면 `AuthenticationFilter`는 로그인 요청에서 `username`과 `password`를 기반으로 인증 객체인 `AuthenticationToken`을 생성한다. `UsernamePasswordAuthenticationFilter`는 `UsernamePasswordAuthenticationToken`을 생성하고, 이를 `AuthenticationManager`에게 인증을 요청한다.
`AuthenticationManager`가 인증에 성공하여 `Authentication` 객체를 반환하면 `AuthenticationFilter`는 `SecurityContext`에 반환받은 `Authentication` 객체를 저장한다.

`Authentication`를 `SecurityContext`에 저장 후, `AuthenticationSuccessHandler`를 실행한다. 인증에 실패하면 `AuthenticationFailureHandler`를 실행한다.

### AuthenticationManager
`AuthenticationManager`는 여러 `AuthenticationProvider`에게 인증을 위임하는 역할을 한다. `AuthenticationManager`는 일반적으로 `ProviderManager`로 구현된다.
`AuthenticationManager`는 여러 `AuthenticationProvider` 중에서 하나라도 인증에 성공하면, 반환받은 `Authentication` 객체를 이벤트 기반으로 `AuthenticationFilter`에 전송한다.
`AuthenticationManager`에 설정된 `AuthenticationProvider` 중, 어떤 것도 인증에 성공하지 못하면 인증은 실패하고 예외를 전달받는다.

### AuthenticationProvider
`AuthenticationProvider`는 `AuthenticationToken`을 통해 실제 인증을 수행하는 객체이다. 사용자 정보를 불러오기 위하여 `UserDetailsService`를 사용하여 인증 정보인 `UserDetails` 객체를 반환받고, `UserDetails`에 담긴 사용자 정보와, `AuthenticationToken`을 통해 인증 로직을 수행한다. 인증에 성공하면 인증된 `Authentication` 객체를 `AuthenticationManager`에게 반환한다.

### UserDetailsService
`UserDetailsService`는 사용자 정보를 불러와서 `UserDetails` 객체를 만들어 반환하는 역할을 한다. `UserDetails` 객체를 `AuthenticationProvider`에 반환하여 `AuthenticationProvider`는 `UserDetails`와 `AuthenticationToken`을 비교하여 인증을 진행한다.


---
## 확장 포인트

### Custom AuthenticationFilter 구현 및 등록
스프링 시큐리티는 기본적으로 `UsernamePasswordAuthenticationFilter`를 통해 인증 과정을 진행한다. 이를 사용하지 않고 JWT 등, 사용자 정의 필터를 만들고 이를 적용하려면 사용자 정의 필터를 만들어 `UsernamePasswordAuthenticationFilter` 이전에 등록하면 된다.

> 필터는 체인 형식으로 여러 필터가 등록되고, 이를 순차적으로 돌면서 필터링을 진행한다.

`Filter`, `GenericFilterBean`, `OncePerRequestFilter` 등을 상속받아 구현하여 사용자 정의 필터를 등록할 수 있다.

`GenericFilterBean`은 스프링에서 제공하는 것으로 스프링 설정 정보를 쉽게 처리할 수 있게 도와준다. `Filter`를 구현한 것과 동일하고 `getFilterConfig`와 `getEnvironment` 메서드를 제공해준다.

`OncePerRequestFilter`는 요청당 한 번의 실행을 보장한다. 이를 사용하면 동일한 요청 내에서 한 번만 해당 필터를 실행하도록 해준다. 예를 들어 인증과 인가를 거치고 특정 URL로 포워딩하면, 서블릿 실행 중 요청이 온 것으로 보고 인증 및 인가 필터를 다시 한번 거치게 된다. `OncePerRequestFilter`를 사용하면 인증과 인가를 한 번만 거칠 수 있게 도와준다.

아래와 같이 구현하고, 이를 빈으로 등록하면 `Filter`가 등록된다.

```java
@Order(-5) // 숫자가 작을수록 먼저 실행된다. -105 보다 큰 값을 사용하는 것을 권장
@Component
public class CustomFilter extends GenericFilterBean {
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
        // 전처리 로직

        chain.doFilter(request, response);

        // 후처리 로직
    }
}

@Order(10) // 숫자가 작을수록 먼저 실행된다. -105 보다 큰 값을 사용하는 것을 권장
@Component
public class CustomFilter extends OncePerRequestFilter {

    @Override
    public void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain) {
        // 전처리 로직

        chain.doFilter(request, response);
        
        // 후처리 로직
    }
}
```

`AbstractAuthenticationProcessingFilter`를 상속받아 구현할 수도 있다.

```java
public class CustomAuthenticationFilter extends AbstractAuthenticationProcessingFilter {

    public CustomAuthenticationFilter(RequestMatcher requiresAuthenticationRequestMatcher) {
        super(requiresAuthenticationRequestMatcher);
    }

    @Override
    public Authentication attemptAuthentication(HttpServletRequest request,
                                                HttpServletResponse response) throws AuthenticationException, IOException, ServletException {
        String email = request.getParameter("username");
        String credentials = request.getParameter("password");

        return getAuthenticationManager().authenticate(new CustomAuthenticationToken(email, credentials));
    }
}
```

스프링 시큐리티에서 특정 필터 전, 후에 커스텀 필터를 추가하고 싶다면 다음과 같이 설정할 수 있다.

```java
@Configuration
@RequiredArgsConstructor
public class SecurityConfig {

    private final CustomFilter customFilter;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .httpBasic()
            .and()
            .formLogin()
            .and()
            .userDetailsService(userDetailsService);

        // UsernamePasswordAuthenticationFilter 전에 CustomFilter를 등록한다.
        http.addFilterBefore(customFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

### AuthenticationProvider 구현 및 등록
`AuthenticationProvider`는 `AuthenticationToken`을 통해 실제 인증을 수행하는 객체이다. 사용자 정보를 불러오기 위하여 `UserDetailsService`를 사용하여 인증 정보인 `UserDetails` 객체를 반환받고, `UserDetails`에 담긴 사용자 정보와, `AuthenticationToken`을 통해 인증 로직을 수행한다. 인증에 성공하면 인증된 `Authentication` 객체를 `AuthenticationManager`에게 반환한다. 이 후 `AuthenticationManager`는 `Filter`에게 인증 객체를 반환, 이를 `SecurityContext`에 저장한다.

```java
@Component
public class CustomAuthenticationProvider implements AuthenticationProvider {

    // 인증 과정을 진행한다.
    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {

        // 인증 로직 구현

        // 인증 객체 리턴;
    }

    // 해당 provider가 인증을 진행할 수 있는지 여부 결정
    // authentication이 CustomAuthenticationToken 클래스 타입이면 해당 provider가 수행된다.
    @Override
    public boolean supports(Class<?> authentication) {
        return CustomAuthenticationToken.class.isAssignableFrom(authentication);
    }
}
```

### UserDetailsService 구현 및 등록
`UserDetailsService`는 사용자 정보를 불러와서 `UserDetails` 객체를 만들어 반환하는 역할을 한다. `UserDetails` 객체를 `AuthenticationProvider`에 반환하면 `AuthenticationProvider`는 `UserDetails`와 `AuthenticationToken`을 비교하여 인증을 진행한다.

```java
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

	private final MemberRepository memberRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Member member = memberRepository.findByUsername(username).orElseThrow();

        return new User(member.getUsername(), member.getPassword(), Collections.singleton(new SimpleGrantedAuthority(member.getRole().name())));
    }
}
```

