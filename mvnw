#!/bin/sh
set -eu

MVNW_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
MVNW_PROPERTIES="$MVNW_ROOT/.mvn/wrapper/maven-wrapper.properties"
MVNW_CACHE="$MVNW_ROOT/.mvn/wrapper/dists"
MVNW_MAVEN_HOME="$MVNW_CACHE/apache-maven-3.9.16"
MVNW_ARCHIVE="$MVNW_CACHE/apache-maven-3.9.16-bin.zip"

read_property() {
    sed -n "s/^$1=//p" "$MVNW_PROPERTIES" | head -n 1
}

MVNW_URL=$(read_property distributionUrl)
MVNW_EXPECTED=$(read_property distributionSha512Sum)

# Alguns ambientes mantêm JAVA_HOME apontando para um JDK já removido. O Maven
# não consegue aplicar o fallback para `java` enquanto essa variável inválida existe.
if [ -n "${JAVA_HOME:-}" ] && [ ! -x "$JAVA_HOME/bin/java" ]; then
    if [ -x /usr/libexec/java_home ]; then
        JAVA_HOME=$(/usr/libexec/java_home 2>/dev/null || true)
        export JAVA_HOME
    else
        unset JAVA_HOME
    fi
fi

if [ ! -x "$MVNW_MAVEN_HOME/bin/mvn" ]; then
    mkdir -p "$MVNW_CACHE"
    if [ ! -f "$MVNW_ARCHIVE" ]; then
        if command -v curl >/dev/null 2>&1; then
            curl -fL "$MVNW_URL" -o "$MVNW_ARCHIVE"
        elif command -v wget >/dev/null 2>&1; then
            wget -O "$MVNW_ARCHIVE" "$MVNW_URL"
        else
            echo "Maven Wrapper requer curl ou wget para o primeiro uso." >&2
            exit 1
        fi
    fi

    if command -v sha512sum >/dev/null 2>&1; then
        MVNW_ACTUAL=$(sha512sum "$MVNW_ARCHIVE" | awk '{print $1}')
    elif command -v shasum >/dev/null 2>&1; then
        MVNW_ACTUAL=$(shasum -a 512 "$MVNW_ARCHIVE" | awk '{print $1}')
    else
        echo "Maven Wrapper requer sha512sum ou shasum para verificar o download." >&2
        exit 1
    fi
    if [ "$MVNW_ACTUAL" != "$MVNW_EXPECTED" ]; then
        echo "Checksum inválido para a distribuição Maven." >&2
        exit 1
    fi
    command -v unzip >/dev/null 2>&1 || {
        echo "Maven Wrapper requer unzip para o primeiro uso." >&2
        exit 1
    }
    unzip -q -o "$MVNW_ARCHIVE" -d "$MVNW_CACHE"
fi

exec "$MVNW_MAVEN_HOME/bin/mvn" "$@"
