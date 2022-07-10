# Querydsl 설정

해당 내용은 김영한님의 *실전! Querydsl*을 수강하고 정리한 내용입니다.

---

## `build.gradle`에 qeurydsl 설정 추가
## 22.07.08 수정함


```gradle
buildscript {
	dependencies {
		classpath("gradle.plugin.com.ewerk.gradle.plugins:querydsl-plugin:1.0.10")
	}
}

plugins {
   id "com.ewerk.gradle.plugins.querydsl" version "1.0.10"
}

apply plugin: "com.ewerk.gradle.plugins.querydsl"

configurations {
	compileOnly {
		extendsFrom annotationProcessor
	}
}

dependencies {
	implementation 'com.querydsl:querydsl-jpa'
	annotationProcessor 'com.querydsl:querydsl-apt'
}

def querydslDir = "$buildDir/generated/querydsl"

querydsl {
	library = "com.querydsl:querydsl-apt"
	jpa = true
	querydslSourcesDir = querydslDir
}

sourceSets {
	main {
		java {
			srcDirs = ['src/main/java', querydslDir]
		}
	}
}

compileQuerydsl{
	options.annotationProcessorPath = configurations.querydsl
}

configurations {
	querydsl.extendsFrom compileClasspath
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

