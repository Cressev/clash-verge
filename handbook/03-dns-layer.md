# 03. DNS Layer

## 目标

避免公司域名和跳板机域名被 Clash fake-ip 污染。

## 典型配置思路

```yaml
dns:
  respect-rules: true
  fake-ip-filter:
    - '*.zphz.cn'
    - jumpserver.zphz.cn
    - feilian.zphz.cn
  nameserver-policy:
    '+.zphz.cn':
      - system
  direct-nameserver:
    - system
  direct-nameserver-follow-policy: true
```

## 关键检查

```powershell
nslookup jumpserver.zphz.cn
```

如果返回 `198.18.x.x` 这类地址，通常说明 fake-ip 还在干活。

## 经验

- 公司域名优先走系统 DNS。
- 飞连相关域名也不要进 fake-ip。
- DNS 层修好后，再看规则和路由是否一致。
