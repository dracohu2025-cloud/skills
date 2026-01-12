# 豆包 TTS 2.0 音色列表

> 官方文档：https://www.volcengine.com/docs/6561/1257544

## 豆包语音合成模型 2.0 音色（uranus_bigtts）

这些是新一代大模型音色，基于豆包大模型技术，具有更自然的情感表达能力。

### 中文女声

| 音色 ID | 名称 | 语言 | 特点 |
|---------|------|------|------|
| `zh_female_vv_uranus_bigtts` | Vivi 2.0 | 中/英 | 自然流畅，支持中英混合 |
| `zh_female_xiaohe_uranus_bigtts` | 小何 2.0 | 中文 | 温柔甜美 |
| `zh_female_wanwanxiaohe_uranus_bigtts` | 湾湾小何 2.0 | 中文 | 台湾腔，温柔甜美 |
| `zh_female_tianmei_uranus_bigtts` | 甜美 2.0 | 中文 | 甜美可爱 |
| `zh_female_qingche_uranus_bigtts` | 清澈 2.0 | 中文 | 清新自然 |

### 中文男声

| 音色 ID | 名称 | 语言 | 特点 |
|---------|------|------|------|
| `zh_male_m191_uranus_bigtts` | 云舟 2.0 | 中文 | 稳重大气 |
| `zh_male_taocheng_uranus_bigtts` | 小天 2.0 | 中文 | 阳光开朗 |
| `zh_male_chunhou_uranus_bigtts` | 醇厚 2.0 | 中文 | 醇厚稳重 |
| `zh_male_qingse_uranus_bigtts` | 青涩 2.0 | 中文 | 青春活力 |

---

## 豆包语音合成模型 1.0 音色（moon_bigtts / saturn_bigtts）

### 中文女声

| 音色 ID | 名称 | 特点 |
|---------|------|------|
| `zh_female_shuangkuaisisi_moon_bigtts` | 爽快思思 | 清爽利落，适合日常对话 |
| `zh_female_tianmeixiaoyuan_moon_bigtts` | 甜美小媛 | 甜美可爱 |
| `zh_female_qingchengjiejie_moon_bigtts` | 倾城姐姐 | 成熟知性 |
| `zh_female_sajiaonvyou_moon_bigtts` | 撒娇女友 | 活泼可爱 |
| `zh_female_qingxinxuemei_moon_bigtts` | 清新学妹 | 青春活力 |
| `zh_female_wenrouxiaoya_moon_bigtts` | 温柔小雅 | 温柔体贴，适合有声书 |
| `zh_female_mizai_saturn_bigtts` | 咪仔 | 活泼俏皮 |

### 中文男声

| 音色 ID | 名称 | 特点 |
|---------|------|------|
| `zh_male_aojiaobazong_moon_bigtts` | 傲娇霸总 | 霸道总裁风 |
| `zh_male_yangguangqingnian_moon_bigtts` | 阳光青年 | 阳光开朗 |
| `zh_male_wenchengwenxi_moon_bigtts` | 文城文熙 | 温文尔雅 |
| `zh_male_chunhouxuedi_moon_bigtts` | 醇厚学弟 | 醇厚稳重 |
| `zh_male_ruyazhanggui_moon_bigtts` | 儒雅掌柜 | 儒雅大方 |
| `zh_male_dayi_saturn_bigtts` | 大义 | 成熟稳重，适合播报 |

### 童声

| 音色 ID | 名称 | 特点 |
|---------|------|------|
| `zh_child_keainvhai_moon_bigtts` | 可爱女孩 | 天真活泼 |
| `zh_child_huoponanhai_moon_bigtts` | 活泼男孩 | 活泼开朗 |

---

## 英文音色

| 音色 ID | 名称 | 特点 |
|---------|------|------|
| `en_female_sarah_moon_bigtts` | Sarah | 美式女声 |
| `en_male_ryan_moon_bigtts` | Ryan | 美式男声 |
| `en_female_amanda_moon_bigtts` | Amanda | 英式女声 |
| `en_male_james_moon_bigtts` | James | 英式男声 |

---

## 你的 .env 配置音色

根据你的配置文件，你正在使用的音色：

| 环境变量 | 音色 ID | 名称 |
|----------|---------|------|
| `VOLCENGINE_TTS_VOICE_TYPE_FEMALE` | `zh_female_mizai_saturn_bigtts` | 咪仔（女声） |
| `VOLCENGINE_TTS_VOICE_TYPE_MALE` | `zh_male_dayi_saturn_bigtts` | 大义（男声） |

---

## 情感参数支持

部分音色支持情感参数：

| 情感 | 参数值 | 说明 |
|------|--------|------|
| 开心 | `happy` | 欢快愉悦 |
| 悲伤 | `sad` | 低沉忧伤 |
| 生气 | `angry` | 愤怒激动 |
| 惊讶 | `surprised` | 惊奇意外 |
| 中性 | `neutral` | 平静自然 |

---

## 使用建议

### 场景推荐

| 场景 | 推荐音色 |
|------|----------|
| 播客/有声书 | `zh_male_dayi_saturn_bigtts`, `zh_female_mizai_saturn_bigtts` |
| 新闻播报 | `zh_male_chunhouxuedi_moon_bigtts` |
| 智能助手 | `zh_female_vv_uranus_bigtts` |
| 广告配音 | `zh_male_aojiaobazong_moon_bigtts` |
| 儿童内容 | `zh_child_keainvhai_moon_bigtts` |
| 中英混合 | `zh_female_vv_uranus_bigtts` |

### 注意事项

1. **2.0 音色**（`uranus_bigtts`）是新一代大模型音色，情感表达更自然
2. **1.0 音色**（`moon_bigtts` / `saturn_bigtts`）是经典音色，稳定可靠
3. 部分 2.0 音色不支持 WebSocket 接口，建议使用 HTTP 接口
4. 2.0 音色目前不支持 SSML

---

## 音色试听

- 控制台试听：https://console.volcengine.com/speech/service/8
- 官方文档：https://www.volcengine.com/docs/6561/1257544

---

*更新日期：2025-12*
