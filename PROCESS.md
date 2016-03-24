To deploy:

```
    git checkout gh-pages-gen
    bundle jekyll build
    git checkout gh-pages
    rm -rf <everything other than _site and CNAME>
    mv _site/* .
```
