# Querydsl 설정

해당 내용은 김영한님의 *실전! Querydsl*을 수강하고 정리한 내용입니다.

---

## `build.gradle`에 qeurydsl 설정 추가



```gradle
buildscript {
   ext {
      queryDslVersion = "5.0.0"
   }
}

plugins {
   id "com.ewerk.gradle.plugins.querydsl" version "1.0.10"
}

dependencies {
   implementation 'com.querydsl:querydsl-jpa:${queryDslVersion}'
   annotationProcessor 'com.querydsl:querydsl-apt:${queryDslVersion}'
}

def querydslDir = "$buildDir/generated/querydsl"

querydsl {
   jpa = true
   querydslSourcesDir = querydslDir
}
sourceSets {
   main.java.srcDir querydslDir
}
configurations {
   querydsl.extendsFrom compileClasspath
}
compileQuerydsl {
   options.annotationProcessorPath = configurations.querydsl
}
```

## 검증용 Q 타입 생성
- 엔티티 작성 후
- Gradle IntelliJ 사용법
  - Gradle -> Tasks -> build -> clean
  - Gradle -> Tasks -> other -> compileQuerydsl
- Gradle 콘솔 사용법
  - `./gradlew clean compileQuerydsl`
- 이후 `build/generated/querydsl`에 `Q-.java`파일이 생성되어 있어야 한다.

