# 04. Rules Layer

规则层负责把目标流量明确送到正确出口。

## 常见规则

```yaml
prepend:
  - 'PROCESS-NAME,corplink-service.exe,DIRECT'
  - 'PROCESS-NAME,corplink-uc.exe,DIRECT'
  - 'PROCESS-NAME,ssh.exe,DIRECT'
  - 'DOMAIN,feilian.zphz.cn,DIRECT'
  - 'DOMAIN-SUFFIX,zphz.cn,DIRECT'
  - 'DOMAIN,jumpserver.zphz.cn,DIRECT'
  - 'IP-CIDR,10.12.0.0/16,DIRECT,no-resolve'
```

## 注意点

- 进程名规则只对真实进程名生效。
- 域名规则只管域名层，不管系统路由。
- 公司内网网段要用 `IP-CIDR`，不要把它写成域名规则。

## 经验

如果公司域名和 SSH 仍然被劫持，常见原因不是规则没写，而是规则写了以后流量还是先被 TUN 截走。
