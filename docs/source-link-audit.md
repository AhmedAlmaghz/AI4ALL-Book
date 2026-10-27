# تدقيق روابط المصادر

- تاريخ التدقيق: 2026-10-27
- المصدر: `docs/fact-check-log.csv` — 257 سجلًا.
- الروابط الفريدة: 136
- المنهج: طلب GET آلي بترويسات متصفح، مع متابعة إعادة التوجيه ومهلة 25 ثانية. النتيجة تتحقق من الاستجابة فقط، لا من مطابقة المحتوى للادعاء.

## 1. الخلاصة

| الحالة | العدد | المعنى |
|---|---|---|
| مستجيب | 97 | استجابة 2xx. |
| إعادة توجيه | 6 | الرابط يعمل لكنه ينتقل إلى عنوان آخر. |
| محجوب آليًا | 21 | 401/403/405/429؛ ليس دليل موت. |
| غير موجود | 0 | 404/410 دون تحقق يدوي. |
| خطأ أو مهلة | 15 | تعذر إكمال الطلب. |
| تحقق يدوي | 3 | أعاد العميل الآلي 404 لكن الصفحة تعمل في المتصفح. |

> «إعادة التوجيه» فئة متقاطعة مع المستجيب أو المحجوب، لا فئة مستقلة؛ لا تُجمع الأرقام جمعًا بسيطًا.

## 2. روابط تحتاج إجراء

### 2.1 غير موجودة (404/410)

لا توجد مدخلات في هذه الفئة.

### 2.2 محجوبة آليًا (ليست دليل موت)

| الرابط | السجلات | الحالة | ملاحظة |
|---|---|---|---|
| https://academic.oup.com/jpart/article/33/1/153/6524536 | FC-0112، FC-0201، FC-0237 | 403 | https://academic.oup.com/jpart/article/33/1/153/6524536 |
| https://academic.oup.com/pages/for-authors/journals/preparing-and-submitting-your-manuscript/ai-principles-for-oxford-journals-authors | FC-0074، FC-0077، FC-0177 | 403 | https://academic.oup.com/pages/for-authors/journals/preparing-and-submitting-your-manuscript/ai-principles-for-oxford-journals-authors |
| https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00369/100684/Sparse-Dense-and-Attentional-Representations-for | FC-0214 | 403 | https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00369/100684/Sparse-Dense-and-Attentional-Representations-for |
| https://dl.acm.org/doi/10.1145/3442188.3445922 | FC-0012، FC-0018 | 403 | https://dl.acm.org/doi/10.1145/3442188.3445922 |
| https://doi.org/10.1080/10463283.2024.2334563 | FC-0251 | 403 | https://www.tandfonline.com/doi/full/10.1080/10463283.2024.2334563 |
| https://doi.org/10.1080/13803611.2024.2363831 | FC-0180 | 403 | https://www.tandfonline.com/doi/full/10.1080/13803611.2024.2363831 |
| https://doi.org/10.1093/mind/LIX.236.433 | FC-0007 | 403 | https://academic.oup.com/mind/article/LIX/236/433/986238 |
| https://doi.org/10.1177/016146811912101102 | FC-0079 | 403 | https://journals.sagepub.com/doi/10.1177/016146811912101102 |
| https://help.openai.com/en/articles/10169521-projects-in-chatgpt | FC-0025، FC-0038 | 403 | https://help.openai.com/en/articles/10169521-projects-in-chatgpt |
| https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt | FC-0123 | 403 | https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt |
| https://help.openai.com/en/articles/8590148-memory-in-chatgpt | FC-0120 | 403 | https://help.openai.com/en/articles/8590148-memory-in-chatgpt |
| https://journals.sagepub.com/doi/10.1111/j.1467-8721.2006.00435.x | FC-0248 | 403 | https://journals.sagepub.com/doi/10.1111/j.1467-8721.2006.00435.x |
| https://onlinelibrary.wiley.com/doi/10.1111/exsy.70221 | FC-0103 | 403 | https://onlinelibrary.wiley.com/doi/10.1111/exsy.70221 |
| https://openai.com/consumer-privacy/ | FC-0004، FC-0037، FC-0229 | 403 | https://openai.com/consumer-privacy/ |
| https://unctad.org/topic/ecommerce-and-digital-economy/ecommerce-law-reform/summary-adoption-e-commerce-legislation-worldwide | FC-0055 | 403 | https://unctad.org/topic/ecommerce-and-digital-economy/ecommerce-law-reform/summary-adoption-e-commerce-legislation-worldwide |
| https://www.coe.int/en/web/freedom-expression/information-disorder | FC-0084 | 403 | https://www.coe.int/en/web/freedom-expression/information-disorder |
| https://www.gao.gov/products/gao-24-107634 | FC-0193، FC-0194 | 403 | https://www.gao.gov/products/gao-24-107634 |
| https://www.sciencedirect.com/science/article/pii/S1747938X26000485 | FC-0236، FC-0242 | 403 | https://www.sciencedirect.com/science/article/pii/S1747938X26000485 |
| https://www.sciencedirect.com/science/article/pii/S2211368120300978 | FC-0087، FC-0138 | 403 | https://www.sciencedirect.com/science/article/pii/S2211368120300978 |
| https://www.w3.org/TR/WCAG22/ | FC-0089، FC-0099 | 403 | https://www.w3.org/TR/WCAG22/ |
| https://www.weforum.org/publications/the-future-of-jobs-report-2025 | FC-0234 | 403 | https://www.weforum.org/publications/the-future-of-jobs-report-2025 |

> «محجوب آليًا» لا يعني أن الرابط ميت؛ تعيد مواقع كثيرة 403 أو 404 لبرامج الزحف.

### 2.3 أخطاء شبكة أو مهلة

| الرابط | السجلات | الحالة | ملاحظة |
|---|---|---|---|
| http://jmc.stanford.edu/articles/dartmouth.html | FC-0008 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html | FC-0256 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://doi.org/10.1016/j.ssaho.2025.102287 | FC-0156، FC-0197 | — | URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)> |
| https://eric.ed.gov/?id=EJ1186664 | FC-0155 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://eric.ed.gov/?id=EJ1414484 | FC-0250 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://eric.ed.gov/?id=EJ1478558 | FC-0154 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf | FC-0227، FC-0231 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html | FC-0016 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://scikit-learn.org/stable/getting_started | FC-0063 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://scikit-learn.org/stable/modules/cross_validation.html | FC-0063 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://scikit-learn.org/stable/modules/model_evaluation.html | FC-0064 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://scikit-learn.org/stable/supervised_learning.html | FC-0013 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://scikit-learn.org/stable/unsupervised_learning.html | FC-0014 | — | URLError: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond> |
| https://www.mckinsey.com/capabilities/transformation/our-insights/common-pitfalls-in-transformations-a-conversation-with-jon-garcia | FC-0218 | — | TimeoutError: The read operation timed out |
| https://www.stlouisfed.org/on-the-economy/2024/sep/rapid-adoption-generative-ai/ | FC-0011 | — | TimeoutError: The read operation timed out |

> الأخطاء والمهل أعلاه تعني أن هذا التدقيق لم يستطع إكمال الطلب من بيئة التشغيل الحالية، ولا تعني بالضرورة أن الرابط ميت. أعِد فحصها قبل الحكم، وسجّل النتيجة اليدوية.

## 3. إعادة التوجيه

| الرابط في السجل | الرابط النهائي | السجلات |
|---|---|---|
| https://doi.org/10.1080/10463283.2024.2334563 | https://www.tandfonline.com/doi/full/10.1080/10463283.2024.2334563 | FC-0251 |
| https://doi.org/10.1080/13803611.2024.2363831 | https://www.tandfonline.com/doi/full/10.1080/13803611.2024.2363831 | FC-0180 |
| https://doi.org/10.1093/mind/LIX.236.433 | https://academic.oup.com/mind/article/LIX/236/433/986238 | FC-0007 |
| https://doi.org/10.1177/016146811912101102 | https://journals.sagepub.com/doi/10.1177/016146811912101102 | FC-0079 |
| https://developers.google.com/search/docs/essentials/spam-policies | https://developers.google.com/search/docs/essentials/spam-policies?hl=ar | FC-0080 |
| https://doi.org/10.1037/0096-1523.1.3.288 | https://doi.apa.org/doi/10.1037/0096-1523.1.3.288 | FC-0206 |

> إعادة توجيه DOI إلى ناشر أمر طبيعي؛ يُبقى رابط DOI لأنه معرّف دائم، ولا يُستبدل بعنوان الناشر إلا إذا تعذّر الوصول.

## 4. تحقق يدوي

| الرابط | تاريخ التحقق | النتيجة |
|---|---|---|
| https://www.ftc.gov/business-guidance/advertising-marketing | 2026-10-27 | صفحة «Advertising and Marketing» مفتوحة في المتصفح رغم 404 للعميل الآلي. |
| https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | 2026-10-27 | دليل CAN-SPAM مفتوح في المتصفح رغم 404 للعميل الآلي. |
| https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers | 2026-10-27 | أسئلة وأجوبة قاعدة المراجعات مفتوحة في المتصفح رغم 404 للعميل الآلي. |
