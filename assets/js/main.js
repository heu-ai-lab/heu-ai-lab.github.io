/* ============================================================
   站点通用脚本：移动端导航 / 当前页高亮 / 新闻渲染 / 入场动画
   ============================================================ */
(function () {
  "use strict";

  /* 1. 移动端导航开关 */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* 2. 当前页面导航高亮（按文件名匹配） */
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a[href]").forEach(function (a) {
    var href = a.getAttribute("href").split("#")[0];
    if (href && href === here) a.classList.add("active");
  });

  /* 3. 新闻动态渲染
        在页面中放 <div class="news-list" data-limit="5"></div> 即可 */
  function renderNews() {
    var mounts = document.querySelectorAll(".news-list");
    if (!mounts.length) return;

    var data = window.LAB_NEWS || [];
    mounts.forEach(function (box) {
      var limit = parseInt(box.getAttribute("data-limit") || "0", 10);
      var items = limit > 0 ? data.slice(0, limit) : data;

      if (!items.length) {
        box.innerHTML = '<p class="empty">暂无动态，敬请期待。</p>';
        return;
      }

      box.innerHTML = items.map(function (n) {
        var title = n.url
          ? '<a class="news-title" href="' + n.url + '" target="_blank" rel="noopener">' + n.title + "</a>"
          : '<span class="news-title">' + n.title + "</span>";
        return (
          '<div class="news-item">' +
          '<div class="news-date">' + n.date + "</div>" +
          "<div>" +
          (n.tag ? '<span class="news-tag">' + n.tag + "</span>" : "") +
          title +
          "</div>" +
          "</div>"
        );
      }).join("");
    });
  }
  renderNews();

  /* 4. 滚动入场动画 */
  var targets = document.querySelectorAll(".reveal");
  if (!targets.length || !("IntersectionObserver" in window)) {
    targets.forEach(function (t) { t.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add("in");
        io.unobserve(en.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

  targets.forEach(function (t, i) {
    t.style.transitionDelay = Math.min(i % 6, 5) * 55 + "ms";
    io.observe(t);
  });
})();
