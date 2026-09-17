# iwlwifi AP teardown: remove group keys before internal stations

**已在一个指定环境验证的驱动修复补丁；源码发布，不是通用二进制驱动。**

This patch addresses a locally reproduced firmware assert (`0x251B`) when stopping a WPA2 AP using the iwlmvm MLD station API. Group keys were still installed when internal multicast stations were removed. The patch queues group-key cleanup before removing those stations. It does not change firmware, regulatory settings or transmit power.

## 问题与修复

非MLO组密钥的link_id为-1，而此环境的链路密钥清理只匹配链路0，导致GTK晚于组播站点删除。诊断显示flush及queue_remove均返回0，随后STA_REMOVE失败；提前清理组密钥后，原版iwlwifi的2.4GHz AP和实验5GHz AP都通过复测。

补丁复用既有密钥清理迭代器并扩展到AP模式，检查内部站点有效性；成功提交删除后使硬件密钥索引失效，避免稍后重复删除。异步命令返回成功仅表示入队，后续同步站点删除成功及无断言才构成进一步验证。

它不是屏蔽断言、加任意延时或跳过站点删除。命令提交失败的所有恢复路径仍未验证。项目不宣称适用于所有固件、所有加密套件或MLO。

## 文件与验证

- [修复补丁](patches/0001.patch)：独立应用，不依赖LARI或诊断补丁。
- [测试范围](docs/TESTING.md)：10项记录场景，以及尚未验证的部分。
- [源码验证](docs/SOURCE.md)、[来源及哈希](SOURCE.json)。
- [GPLv2](LICENSE)、[版权来源](NOTICE)、[担保说明](DISCLAIMER.md)。

源码基线：backports 6.12.96。修改日期：2026-09-18。尚未提交或获得上游维护者认可。

5GHz LARI实验独立发布在 [ax411-lari-5ghz-research](https://github.com/zhangzexin/ax411-lari-5ghz-research)。本修复不需要它，也不解决该实验的信道策略或认证问题。
