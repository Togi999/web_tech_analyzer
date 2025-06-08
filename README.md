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
```

## Kullanım

```bash
python webtech_analyzer.py
```

- Program çalıştıktan sonra:

Hedef URL girmeniz istenir.
Ardından çıktı formatı olarak json, pdf veya her ikisi tercihinizi yaparsınız.
Raporlar report.json ve/veya report.pdf olarak oluşturulur.


## Gereksinimler

```bash
Python 3.x
requests
beautifulsoup4
fpdf
```

- Hepsi requirements.txt dosyasında yer almaktadır. Yüklemek için:
```bash
pip install -r requirements.txt
```

## signatures.json Çıktı Örneği

```bash
{
  "Apache": {
    "headers": ["Server"],
    "html_patterns": ["Apache"],
    "meta_generator": []
  },
  "WordPress": {
    "headers": ["X-Powered-By"],
    "html_patterns": ["wp-content", "wp-includes"],
    "meta_generator": ["WordPress"]
  }
}
```

## Çıktı Örneği

```bash
[+] Analiz ediliyor: https://orneksite.com

[+] Tespit Edilen Teknolojiler:
 - Server: Apache
 - CSS Framework: Bootstrap (https://orneksite.com/css/bootstrap.min.css)
 - JavaScript Library: https://orneksite.com/js/jquery.min.js
 - Login Page Detected: WordPress Login

[+] JSON raporu oluşturuldu: report.json
[+] PDF raporu oluşturuldu: report.pdf
```

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.

## Sorumluluk Reddi

Bu proje sadece eğitim ve analiz amaçlıdır. Kullanıcılar, yazılımı kendi sorumlulukları altında kullanır. Yazılımın kullanımından doğabilecek herhangi bir zarar veya kayıptan proje sahibi sorumlu tutulamaz.

