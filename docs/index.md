---
hide:
#   - navigation
#   - toc
  - footer
# YAML front matter中的title用于生成页面的元数据，如浏览器标签、导航链接
title: smileatlRepo
template: home.html
---

<!-- 隐藏h1标题，h1标题在mkdocs中有写就会显示在页面左上 -->
<!-- <h1 style="display:none">smileatlRepo</h1> -->
<!-- 完全透明 -->
<!-- <h1 style="opacity: 0;">smileatlRepo</h1> -->
<!-- 单纯的居中显示的字 -->
<center><font  color= #518FC1 size=6 class="ml3">smileatl Repository</font></center>

<!-- margin-left偏移一点位置 -->
<!-- <h1 style="text-align:center; margin-left: 55px; color:#518FC1; font-size:2em;" class="ml3">smileatl Repository</h1> -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/2.0.2/anime.min.js"></script>

<p align="center">
  smileatl 个人知识库，Welcome！在广袤的空间和无限的时间中，能与你共享同一颗行星与同一段时光是我的荣幸。
</p>

<div id="rcorners">
    <body>
      <font color="#4351AF">
        <p class="p1"></p>
<script defer>
    //格式：2020年04月12日 10:20:00 星期二
    function format(newDate) {
        var day = newDate.getDay();
        var y = newDate.getFullYear();
        var m =
            newDate.getMonth() + 1 < 10
                ? "0" + (newDate.getMonth() + 1)
                : newDate.getMonth() + 1;
        var d =
            newDate.getDate() < 10 ? "0" + newDate.getDate() : newDate.getDate();
        var h =
            newDate.getHours() < 10 ? "0" + newDate.getHours() : newDate.getHours();
        var min =
            newDate.getMinutes() < 10
                ? "0" + newDate.getMinutes()
                : newDate.getMinutes();
        var s =
            newDate.getSeconds() < 10
                ? "0" + newDate.getSeconds()
                : newDate.getSeconds();
        var dict = {
            1: "一",
            2: "二",
            3: "三",
            4: "四",
            5: "五",
            6: "六",
            0: "天",
        };
        //var week=["日","一","二","三","四","五","六"]
        return (
            y +
            "年" +
            m +
            "月" +
            d +
            "日" +
            " " +
            h +
            ":" +
            min +
            ":" +
            s +
            " 星期" +
            dict[day]
        );
    }
    var timerId = setInterval(function () {
        var newDate = new Date();
        var p1 = document.querySelector(".p1");
        if (p1) {
            p1.textContent = format(newDate);
        }
    }, 1000);
</script>
      </font>
    </body>
  </div>

<!-- <p align="center">

  <a href="site_introduction/">
    <img src="https://www.hello-algo.com/index.assets/btn_read_online_dark.svg" width="145"></a>
  <a href="about/">
    <img src="https://www.hello-algo.com/index.assets/btn_download_pdf_dark.svg" width="145"></a>
</p> -->

<p align="center">
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=518FC1&center=true&vCenter=true&width=435&height=60&lines=Welcome+to+smileatlRepo!" alt="Typing SVG" /></a>
  </br>
  <!-- 相对路径跳转 -->
  <a href="start_learning/" class="rounded-button blue-button">
      <span>开始学习</span>
  </a>
  <a href="about/" class="rounded-button gray-button">
      <span>关于网站</span>
  </a>
</p>

<!-- <p align="center">
  <a href="start_learning/" class="rounded-button blue-button">
      <span>开始学习</span>
  </a>
  <a href="about/" class="rounded-button gray-button">
      <span>关于网站</span>
  </a>
</p> -->
