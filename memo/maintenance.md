## 概要
Python 開発環境のメンテナンス(Mac 用)

## Homebrew
```
% brew update
% brew outdated
% brew upgrade
% brew cleanup
```

## pip
* 事前に `pip install pip-review` しておく
```
$ pip3 install --upgrade pip
$ pip-review --auto
```

## 参考
* macOS Big Sur にアップグレードした後にpyenv installできなくなった際の私の場合の解決方法
    * https://qiita.com/hisa_shim/items/abb4936f1f676fe6a7b8