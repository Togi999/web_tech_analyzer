# Web Teknoloji Analiz Aracı

Bu proje, hedef bir web sitesinde kullanılan teknolojileri tespit eden bir analiz aracıdır. HTTP başlıklarını, HTML içeriğini, JavaScript kütüphanelerini, CSS framework’lerini ve CMS giriş sayfalarını analiz eder. Ayrıca varsa lisans dosyalarını da algılar. Çıktı olarak JSON ve/veya PDF raporları üretir.

## Özellikler

- HTTP başlık analizleri
- Meta tag ve HTML pattern analizi
- JavaScript/CSS kütüphane tespiti
- CMS giriş sayfası kontrolü
- Lisans dosyası kontrolü (`/license`, `LICENSE.txt`, vb.)
- CDN/WAF tespiti (Cloudflare, Sucuri, AWS, vb.)
- JSON ve PDF formatında rapor üretimi

## Kurulum

```bash
git clone https://github.com/kullanici-adi/web-tech-analyzer.git
cd web-tech-analyzer
pip install -r requirements.txt
