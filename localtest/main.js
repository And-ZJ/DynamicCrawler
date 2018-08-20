function dynamicImg(img_url)
{
    var div = document.createElement("div");
    div.innerText = img_url;
    var img = document.createElement("img");
    img.src = img_url;
    img.classList.add("test");
    document.body.appendChild(div);
    document.body.appendChild(img);
}
// 用js在页面上添加两张图片
dynamicImg("./test1.png");
dynamicImg("./test2.bmp");