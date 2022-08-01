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

### UserDetailsServices





---
## 확장 포인트
