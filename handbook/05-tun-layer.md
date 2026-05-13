# 05. TUN Layer

## 目标

避免 Clash Verge 的 TUN 先抢走本该走飞连的流量。

## 关键做法

```yaml
tun:
  route-exclude-address:
    - 198.18.0.12/32
    - 117.50.188.56/32
    - 10.12.0.0/16
```

## 为什么只写 `DIRECT` 不够

因为 `DIRECT` 只是规则层的结果，不代表系统路由没被 TUN 接管。

## 经验

- 目标网段进了 `route-exclude-address`，系统路由才更像“真的绕过了 Clash TUN”。
- 如果跳板机有固定公网 IP，也可以临时加进去，但要复查，别把临时值当永久常量。
