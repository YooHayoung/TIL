# AuthenticationPrincipal

`AuthenticationFilter`를 통해 로그인을 성공적으로 마쳤다면 `UserDetailService`에서 반환한 객체가 `SecurityContext`에 저장된다. 

> `UserDetailService`는 사용자 정보를 불러와서 `UserDetails` 객체를 만들어 반환하는 역할을 한다. 실제 인증 과정은 `AuthenticationProvider`가 `UserDetailService`에서 반환한 `UserDetails` 객체를 통하여 수행한다.

`Controller`에서 로그인한 사용자의 정보를 파라미터로 받고 싶다면 다음과 같이 `Principal` 객체로 받아서 사용할 수 있다. `Principal`은 `SecurityContext`에서 로그인된 사용자 정보를 받아온다.

```java
@GetMapping("/")
public String indexPage(Model model, Principal principal) {
	if (principal != null) {
		model.addAttribute("username", principal.getName());
	}
	return "index";
}
```

하지만 `Principal`에서 참조할 수 있는 정보는 `name` 정보밖에 없기 때문에 상당히 제한적이다.

## @AuthenticationPrincipal
`@AuthenticationPrincipal` 애노테이션을 사용하면 `UserDetailService`에서 반환한 객체를 직접 받아 사용할 수 있다. `UserDetailService`는 `loadUserByUsername` 메서드를 통해 `<interface> UserDetail`을 반환한다. 스프링 시큐리티는 `<interface> UserDetail`의 구현체인 `org.springframework.security.core.userdetails.User`를 제공한다. 따라서 `UserDetailService.loadUserByUsername` 메서드의 반환값으로 `User`를 반환하면, `@AuthenticationPrincipal`을 통해 로그인 된 사용자의 정보(`User`)를 `SecurityContext`에서 꺼내서 사용할 수 있다.

```java
/// UserDetailsService 구현
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

	private final MemberRepository memberRepository;

  @Override
  public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
      Member member = memberRepository.findByUsername(username).orElseThrow();
      return new User(member.getUsername(), member.getPassword(), Collections.singleton(new SimpleGrantedAuthority(member.getRole().name())));
  }
}

// Controller
@GetMapping("/")
public String indexPage(Model model, @AuthenticationPrincipal User user) {
	if (user != null) {
		model.addAttribute("username", user.getUsername());
		model.addAttribute("password", user.getPassword());
	}
	return "index";
}
```



### UserAdaptor
`User` 클래스는 개발자가 작성한 `domain` 객체가 아니다. `User` 클래스에는 로그인된 사용자의 인증과 권한 관리를 위한 `username`, `password`, `role` 만을 갖는다. `domain` 객체가 아니기 때문에 `domain` 객체의 다른 정보는 갖고있지 않다. `SecurityContext`에 `domain` 정보를 포함한 `User` 객체를 저장해두고, 이를 꺼내어 사용하려면 `User` 클래스를 상속받은 `Adaptor` 클래스를 만들고, 해당 클래스의 필드에 `domain` 객체를 두어, 이를 꺼내서 사용하면 된다.

```java
// User를 상속받은 UserAdaptor 클래스
// UserDetailsService에서 이를 반환하면 SecurityContext에 UserAdaptor가 저장된다.
// UserAdaptor는 User를 상속받았고, User는 UserDetail 인터페이스를 구현한 구현체이다.
@Getter
public class UserAdaptor extends User {

  private Member member;

  public UserAdaptor(Member member) {
      super(member.getUsername(), member.getPassword(), Collections.singleton(new SimpleGrantedAuthority(member.getRole().name())));
      this.member = member;
  }
}

/// UserDetailsService 구현
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

	private final MemberRepository memberRepository;

  @Override
  public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
      Member member = memberRepository.findByUsername(username).orElseThrow();
      return new UserAdaptor(member);
  }
}

// Controller
@GetMapping("/")
public String indexPage(Model model, @AuthenticationPrincipal UserAdaptor userAdaptor) {
	if (userAdaptor != null) {
		// UserAdaptor의 필드에는 로그인된 Member가 있다. 이를 꺼내어 쓰면 된다.
		model.addAttribute("member", userAdaptor.getMember());
	}
	return "index";
}
```

`UserAdaptor`를 통해서 내부에 `domain` 객체를 두고, 이를 꺼내어 사용할 수 있다. 하지만 `domain` 객체를 사용하려면 계속 `Adaptor`를 통해 접근해야 한다는 문제가 있다. 이를 해결하여 `Adaptor` 내부의 `domain` 객체를 직접 받을 수 있는 방법은 `@AuthenticationPrincipal` 애노테이션이 지원하는 SpEL을 사용하는 것이다.

`@AuthenticationPrincipal`은 SpEL을 지원한다. 이를 사용하여 `Adaptor` 내부의 `domain` 객체를 직접 반환받을 수 있다.

```java
@GetMapping("/")
public String indexPage(Model model, 
			@AuthenticationPrincipal(expression = "#this == 'anonymousUser' ? null : member") Member member) {
	if (member != null) {
		model.addAttribute("member", member);
	}
	return "index";
}
```

스프링 시큐리티는 로그인된 사용자가 아니면 `AnonymousAuthenticationFilter`에 의해 `Authentication`을 생성하고 `anonymous`라는 이름으로 `SecurityContext`에 저장한다. 따라서 해당 SpEL 표현식은 현재 참조중인 객체가 `AnonymousAuthenticationFilter`에 의해 생성된 `Authentication` 이라면 `null`을 반환하고, 아니면 `UserAdaptor` 객체로 간주하여, 내부의 `Member` 객체를 반환하라는 의미이다.

`@AuthenticationPrincipal`의 SpEL을 통해 `Adaptor` 내부의 `domain` 객체를 직접 반환받아 사용할 수 있다. 하지만 이를 위한 SpEL 표현식이 너무 길어 사용하기 불편하다. 다음과 같이 커스텀 애노테이션을 생성하여 편리하게 사용하도록 하자.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
@AuthenticationPrincipal(expression = "#this == 'anonymousUser' ? null : user")
public @interface AuthMember {
}
```
