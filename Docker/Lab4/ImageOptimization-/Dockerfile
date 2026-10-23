# -----------------------------
# Stage 1: Build the Application
# -----------------------------
FROM maven:3.9.15-eclipse-temurin-17-alpine AS builder

WORKDIR /build

# نسخ ملفات المشروع
COPY pom.xml .
COPY src ./src

# بناء ملف الـ JAR وتخطي التيست لتسريع العملية
RUN mvn clean package -DskipTests

# -----------------------------
# Stage 2: Minimal Runtime Environment
# -----------------------------
FROM eclipse-temurin:17-jre-alpine

# إنشاء يوزر ومجموعة غير روت (non-root) للأمان
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# نسخ ملف الـ JAR الناتج فقط من الـ builder stage
COPY --from=builder /build/target/demo-0.0.1-SNAPSHOT.jar app.jar

# تغيير ملكية الملفات لليوزر الجديد
RUN chown -R appuser:appgroup /app

# التحويل لليوزر العادي
USER appuser

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]