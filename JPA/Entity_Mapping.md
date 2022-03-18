# Entity Mapping

## @Entity
- JPA가 관리하는 클래스에 붙인다.
- JPA를 사용하여 테이블과 매핑할 클래스는 @Entity 필수임
- JPA spec상 public or protected 기본 생성자 필요하다.
- final 클래스, enum, interface, inner 클래스 사용 불가
- 저장할 필드에 final 사용 불가

<br>

## 매핑 어노테이션 정리
- @Column <br> 컬럼 매핑
- @Temporal <br> 날짜 타입 매핑 (요즘엔 LocalDateTime을 사용해서 잘 안쓴다)
- @Enumerated
  - enum 타입 매핑
  - value 속성에 ORDINAL이 아닌 STRING을 사용하자.
  - ORDINAL 사용하면 enum 값이 변경될 시에 순서가 변경될 우려가 있다.
- @Lob <br> BLOB, CLOB 매핑
- @Transient <br> 특정 필드를 컬럼에 매핑하지 않는다.

<br>






<br><br><br><br>

---

해당 내용은 김영한님의 강의를 듣고 정리한 내용입니다.