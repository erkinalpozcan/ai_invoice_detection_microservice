# 🚀 AI-Powered Invoice Processing Microservice (YOLO & OCR)

Bu proje, faturalardaki önemli bilgileri otomatik olarak algılamak ve metinleri çıkarmak için Gelişmiş Bilgisayar Görüşü (Computer Vision) tekniklerini ve Mikroservis Mimarisini bir araya getiren kapsamlı bir çözümdür. Proje, modern bulut teknolojileri (Azure Kubernetes Service, Azure Container Registry) ve sürekli entegrasyon/teslimat (CI/CD) pipeline'ları kullanılarak ölçeklenebilirlik, esneklik ve otomatik dağıtım yetenekleri ile tasarlanmıştır.

## ✨ Temel Özellikler

* **Nesne Algılama (Object Detection):** YOLO (You Only Look Once) modeli kullanarak fatura üzerindeki anahtar alanları (örneğin, fatura numarası, toplam tutar, tarih) otomatik olarak algılar.
* **Optik Karakter Tanıma (OCR):** Algılanan alanlardaki metinleri yüksek doğrulukla dijital metne dönüştürür.
* **Mikroservis Mimarisi:** Proje, görevleri ayrıştırılmış ve bağımsız servisler (YOLO, OCR, Main) halinde organize ederek esnekliği ve bakımı kolaylaştırır.
* **API Tabanlı Erişim:** Tüm servisler, RESTful API'ler aracılığıyla iletişim kurar ve dış sistemler tarafından kolayca entegre edilebilir.
* **Bulut Yerel Dağıtım:** Uygulama, Azure Kubernetes Service (AKS) üzerinde çalıştırılmak üzere tasarlanmıştır, bu da yüksek erişilebilirlik ve otomatik ölçeklendirme sağlar.
* **Otomatik CI/CD Pipeline:** GitHub Actions kullanarak kod değişikliklerinden üretime kadar olan süreci otomatikleştirir, hızlı ve güvenilir dağıtımlar sağlar.

## 💡 Kullanılan Teknolojiler

Bu proje, aşağıdaki anahtar teknolojileri kullanarak geliştirilmiş ve dağıtılmıştır:

* **Python:** Uygulama mantığı ve servisler Python ile yazılmıştır.
* **FastAPI & Uvicorn:** Yüksek performanslı ve modern web API'leri oluşturmak için kullanılmıştır.
* **Ultralytics YOLO:** Nesne algılama görevleri için YOLOv8 gibi son teknoloji modellerden yararlanır.
* **OpenCV:** Görüntü işleme görevleri için temel kütüphane.
* **[OCR Kütüphanesi/API Adı]:** Metin tanıma işlemleri için kullanılan kütüphane/servis. (Örn: Tesseract, Azure AI Vision, PaddleOCR)
* **Docker:** Uygulama servislerini izole ve taşınabilir kapsayıcılarda paketlemek için.
* **Kubernetes (K8s):** Kapsayıcılı uygulamaların dağıtımı, ölçeklendirilmesi ve yönetimi için orkestrasyon platformu.
* **Azure Kubernetes Service (AKS):** Azure bulutunda yönetilen Kubernetes hizmeti.
* **Azure Container Registry (ACR):** Docker imajlarını güvenli ve özel olarak depolamak için.
* **GitHub Actions:** Sürekli Entegrasyon ve Sürekli Teslimat (CI/CD) pipeline'ı için.
* **Microsoft Azure:** Tüm bulut altyapısı ve servisleri bu platformda barındırılmaktadır.

## 🏗️ Proje Mimarisi ve Yapısı

Proje, üç ana mikroservis ve Kubernetes dağıtım dosyalarından oluşmaktadır:


* **`yolo_service`**: Gelen görüntüleri alır, YOLO modeli ile nesne algılama yapar ve tespit edilen kutu koordinatlarını döndürür.
* **`ocr_service`**: Belirli görüntü bölgelerinden (YOLO tarafından belirlenen) metinleri çıkarır.
* **`main_service`**: Kullanıcı isteklerini alır, YOLO ve OCR servislerini orkestre eder, iş akışını yönetir ve nihai fatura bilgilerini döndürür. Bu servis aynı zamanda uygulamanın dış dünyaya açılan ana API kapısıdır.

Main servis, Kubernetes'in dahili DNS keşfi sayesinde `yolo-service` ve `ocr-service`'e erişir.

## 🚀 Yerel Olarak Çalıştırma (Docker Compose ile)

Projenin mikroservis yapısı sayesinde, tüm servisi Docker Compose kullanarak yerel makinenizde kolayca çalıştırabilirsiniz:

1.  **Gereksinimler:**
    * Docker Desktop kurulu ve çalışıyor olmalı.
    * Projenin tüm klasörlerini klonlayın: `git clone https://github.com/erkinalpozcan/ai_invoice_detection_microservice.git`
    * Proje dizinine gidin: `cd ai_invoice_detection_microservice`

2.  **Servisleri Başlatma:**
    * Projenin ana dizininde ( `docker-compose.yaml` dosyasının bulunduğu yerde) aşağıdaki komutu çalıştırın:
        ```bash
        docker-compose up --build
        ```
    * Bu komut, Docker imajlarını oluşturacak ve tüm servisleri başlatacaktır.

3.  **API'ye Erişim:**
    * Servisler başlatıldıktan sonra, ana API'ye ve Swagger arayüzüne tarayıcınızdan erişebilirsiniz:
        * Ana API (Swagger UI): `http://localhost:8003/docs`

## ☁️ Azure'a Dağıtım (GitHub Actions CI/CD ile)

Bu proje, kod değişikliklerini otomatik olarak veya manuel tetiklemeyle Azure Kubernetes Service (AKS) üzerine dağıtan bir CI/CD pipeline'ına sahiptir. Bu, geliştirme hızını artırır ve insan hatasını azaltır.

### Dağıtım Ön Koşulları (Yeni Bir Ortama Dağıtacaklar İçin)

Projenin CI/CD pipeline'ını kendi Azure hesabınıza dağıtmak istiyorsanız, aşağıdaki Azure kaynaklarına ve ayarlarına ihtiyacınız olacaktır:

1.  **Azure Hesabı ve Aboneliği:** Aktif bir Azure aboneliğiniz olmalı.
2.  **Azure CLI:** Bilgisayarınızda Azure CLI yüklü ve yapılandırılmış olmalı.
3.  **GitHub Deposu:** Bu projeyi kendi GitHub hesabınıza fork etmiş veya klonlamış olmalısınız.
4.  **Azure Kaynakları:**
    * Bir **Kaynak Grubu** (Örn: `myResourceGroup`)
    * Bir **Azure Container Registry (ACR)** (Örn: `faturaacr`)
        * ACR'nin yönetici kullanıcısı (Admin user) etkinleştirilmiş olmalı.
    * Bir **Azure Kubernetes Service (AKS) Kümesi** (Örn: `faturaaks`)
        * AKS kümesi, oluşturduğunuz ACR ile ilişkilendirilmiş olmalı (`az aks update --attach-acr`).
        * AKS düğüm havuzu için uygun bir VM boyutu seçmeli (örneğin `Standard_D4s_v4` veya `Standard_B2s` gibi CPU tabanlı VM'ler veya GPU tabanlı iş yükleri için `Standard_NC4as_T4_v3` gibi VM'ler).
5.  **Kubernetes YAML Dosyaları:** Projenin `k8s/` dizinindeki YAML dosyaları, imaj yollarınızı doğru ACR adresleriyle güncellediğinizden emin olun (Örn: `faturaacr.azurecr.io/faturayolo-yolo_service:app`).

### GitHub Actions İçin Sırları Yapılandırma

GitHub Actions'ın Azure kaynaklarınıza güvenli bir şekilde erişebilmesi için gerekli kimlik bilgilerini GitHub Secrets olarak eklemelisiniz.

1.  **Azure Service Principal Oluşturun:**
    Azure CLI'da aşağıdaki komutu çalıştırarak bir hizmet sorumlusu (Service Principal) oluşturun. Bu, GitHub Actions'ın Azure'da sizin adınıza işlem yapmasını sağlar.
    ```bash
    az ad sp create-for-rbac --name "github-actions-sp" --role contributor --scopes /subscriptions/<YOUR_SUBSCRIPTION_ID>/resourceGroups/<YOUR_RESOURCE_GROUP_NAME> --sdk-auth
    ```
    Komutun çıktısındaki **tüm JSON bloğunu kopyalayın.** (Bu, `AZURE_CREDENTIALS` sırrı olacak).

2.  **GitHub Deponuza Sırları Ekleyin:**
    Kendi GitHub deponuza gidin: **Settings (Ayarlar) > Secrets and variables (Sırlar ve Değişkenler) > Actions (Eylemler)** bölümüne tıklayın ve aşağıdaki sırları ekleyin (kendi değerlerinizle doldurun):

    * `AZURE_CREDENTIALS`: Yukarıdaki JSON çıktısının tamamı.
    * `AZURE_RESOURCE_GROUP`: `myResourceGroup` (veya kendi kaynak grubunuzun adı)
    * `AZURE_AKS_NAME`: `faturaaks` (veya kendi AKS kümenizin adı)
    * `AZURE_ACR_NAME`: `faturaacr` (veya kendi ACR'nizin adı)
    * `ACR_SECRET_USERNAME`: ACR yönetici kullanıcı adınız (`az acr credential show --name <ACR_NAME> --query username --output tsv` ile alabilirsiniz).
    * `ACR_SECRET_PASSWORD`: ACR yönetici parolanız (`az acr credential show --name <ACR_NAME> --query "passwords[0].value" --output tsv` ile alabilirsiniz).
    * `ACR_SECRET_EMAIL`: Herhangi bir geçerli e-posta adresi (örneğin: `no-reply@github.com`).

### Dağıtım Pipeline'ını Başlatma (Manuel)

1.  **Kod Değişikliklerini Push Et:** Herhangi bir kod değişikliği yaptığınızda veya sadece pipeline'ı çalıştırmak istediğinizde, değişiklikleri GitHub deponuzdaki `main` branch'ine push edin:
    ```bash
    git add .
    git commit -m "Update application code or trigger deployment"
    git push origin main
    ```
    (GitHub Actions, `workflow_dispatch` tetikleyicisi nedeniyle bu push ile otomatik olarak başlamaz.)

2.  **Workflow'u Manuel Olarak Tetikle:**
    * GitHub deponuza gidin.
    * **"Actions" (Eylemler)** sekmesine tıklayın.
    * Sol taraftaki iş akışları listesinden **"Deploy to Azure AKS (Manual)"** iş akışını seçin.
    * Sağ üstte **"Run workflow" (İş akışını çalıştır)** düğmesine tıklayın.
    * Dağıtım yapmak istediğiniz branch'i (`main`) seçin ve "Run workflow" düğmesine tekrar tıklayarak pipeline'ı başlatın.

3.  **Dağıtım Durumunu Kontrol Et:**
    * GitHub Actions sayfasında çalışmanın ilerlemesini izleyin. Tüm adımların yeşil tik (✓) ile tamamlandığından emin olun.
    * Azure CLI'da pod ve servis durumlarını kontrol edin:
        ```bash
        kubectl get pods
        kubectl get services
        ```
    * `main-service` için atanan `EXTERNAL-IP` adresini not alın.

### 🌐 API Erişimi

Uygulamanız başarıyla dağıtıldıktan sonra, ana API'ye ve Swagger arayüzüne `main-service`'in dış IP adresi üzerinden erişebilirsiniz:

* **Swagger UI:** `http://[YOUR_MAIN_SERVICE_EXTERNAL_IP]:8003/docs`
    * `[YOUR_MAIN_SERVICE_EXTERNAL_IP]` yerine `kubectl get services` çıktısındaki IP adresini yazın.


## 📧 İletişim

* **Erkinalp Özcan** - erkinalpozcan@gmail.com
* **LinkedIn:** https://www.linkedin.com/in/erkinalpozcan/
* **GitHub:** https://github.com/erkinalpozcan

Projemi incelediğiniz için teşekkür ederim!

---
