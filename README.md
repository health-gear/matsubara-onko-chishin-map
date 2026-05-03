# 📍 松原市 温故知新マップ (Matsubara Onko-Chishin Map)

🌐 **App URL:** [https://health-gear.github.io/matsubara-onko-chishin-map/](https://health-gear.github.io/matsubara-onko-chishin-map/)

大阪府松原市の公式オープンデータ「まつばらいろはかるた」を活用した、子ども・市民向けの歴史探索AIマップアプリです。
シビックテック・コミュニティ「[Code for Matsubara](https://codeformatsubara.org)」の有志エンジニアにより、週末ハッカソンを通じて企画・開発されました。

## 概要 (Overview)
「地域の歴史や文化財を、テクノロジーの力でもっと身近に」をコンセプトに開発されたWebアプリケーションです。
スマートフォンのGPS機能とAI（自然言語処理）を組み合わせることで、市民が街を歩きながら松原市の魅力や歴史を楽しく学べる体験を提供します。

## 主な機能 (Features)
* 🗺️ **オープンデータの地図化:** 松原市が公開する「まつばらいろはかるた」の座標データを地図上にマッピング。
* 🤖 **AIによる解説機能:** 難しい歴史の言葉や文化財の背景を、子どもにも分かりやすい言葉でAIが解説します。
* 📍 **現在地ナビゲーション:** Geolocation APIを活用し、ユーザーの現在地から近い文化財を案内します。
* 🛡️ **セキュアな設計 (Client-Side Only):** 本アプリはバックエンド（独自のデータベース）を持たず、ブラウザ上で完結するSPA（Single Page Application）として設計されています。利用者の個人情報や位置情報が外部サーバーに保存されることは一切ないため、教育現場でも安心してご利用いただけます。

## 開発の背景 (Background)
本アプリは、地域課題をITで解決する「シビックテック（Civic Tech）」のアプローチを実証するために開発されました。
行政のオープンデータを活用し、市民エンジニアが自らの手でコードを書くことで、開発・運用コストをかけることなく地域のDX（デジタルトランスフォーメーション）を推進するモデルケースを目指しています。

## 技術スタック (Tech Stack)
* **Frontend:** HTML5, CSS3 (Tailwind CSS), JavaScript
* **Map & Location:** Leaflet.js / Geolocation API
* **Data Source:** 松原市オープンデータ（まつばらいろはかるた CSV）
* **Hosting:** GitHub Pages (Serverless)

## 開発・運営体制 (Maintainer)
本プロジェクトは、松原市のシビックテック推進コミュニティによってメンテナンスされています。

* **Organization:** [Code for Matsubara](https://codeformatsubara.org)
* **Lead Engineer:** Takafumi Maruyoshi ([@health-gear](https://github.com/health-gear))

## ライセンス・クレジット (License & Attribution)
本アプリケーションのソースコード自体は [MIT License](LICENSE) の下で公開されています。どなたでも自由に改変・再配布が可能です。

**【オープンデータのクレジット表記】**
本アプリケーション内で使用している「まつばらいろはかるた」のデータおよび画像は、松原市が提供するオープンデータを活用しています。
* **データ出典:** 松原市 オープンデータ（まつばらいろはかるた）
* 本データは [クリエイティブ・コモンズ 表示 4.0 国際 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.ja) ライセンスの下に提供されています。
