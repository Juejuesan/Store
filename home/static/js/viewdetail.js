let currentItemIndex=0;
const totalItems=document.querySelectorAll('.item-slide').length;

document.addEventListener('click',function(e){
    var t=e.target;
    if(t.classList.contains('thumbnail')){
        var s=t.closest('.item-slide'),i=s.querySelector('.main-image');
        i.style.opacity='0';
        setTimeout(function(){i.src=t.src;i.style.opacity='1'},150);
        s.querySelectorAll('.thumbnail').forEach(function(e){e.classList.remove('active')});
        t.classList.add('active');
    }
    if(t.classList.contains('size-btn')&&!t.classList.contains('sold-out')){
        var s=t.closest('.item-slide'),id=s.id.replace('itemSlide','');
        s.querySelectorAll('.size-btn').forEach(function(e){e.classList.remove('active')});
        t.classList.add('active');
        var pr=document.getElementById('itemPrice'+id),inf=document.getElementById('sizeInfo'+id);
        if(pr)pr.textContent=t.dataset.price+' MMK';
        if(inf)inf.innerHTML='Size: <strong>'+t.dataset.size+'</strong> | Price: <strong>'+t.dataset.price+' MMK</strong> | Stock: <strong>'+t.dataset.quantity+'</strong>';
    }
    if(t.closest('#prevBtn'))navigateItem(-1);
    if(t.closest('#nextBtn'))navigateItem(1);
    if(t.closest('.wishlist-btn')){
        var b=t.closest('.wishlist-btn');
        b.classList.toggle('liked');
        var ic=b.querySelector('i'),sp=b.querySelector('span');
        if(b.classList.contains('liked')){ic.className='fa-solid fa-heart';sp.textContent='Saved';}
        else{ic.className='fa-regular fa-heart';sp.textContent='Wishlist';}
    }
    if(t.classList.contains('qty-btn')){
        var s=t.closest('.item-slide'),id=s.id.replace('itemSlide','');
        var inp=document.getElementById('qty'+id);
        var d=t.textContent.trim()==='+'?1:-1;
        var v=parseInt(inp.value)+d;
        if(v<1)v=1;if(v>99)v=99;
        inp.value=v;
    }
    if(t.closest('.add-cart-btn')){
        var s=t.closest('.add-cart-btn').closest('.item-slide'),id=s.id.replace('itemSlide','');
        var qty=document.getElementById('qty'+id).value;
        var name=s.querySelector('.item-title').textContent;
        var sz=s.querySelector('.size-btn.active');
        var msg='Added '+qty+' x '+name;
        if(sz)msg+=' (Size: '+sz.dataset.size+')';
        msg+=' to cart!';
        alert(msg);
    }
});

function navigateItem(d){
    var n=currentItemIndex+d;
    if(n<0||n>=totalItems)return;
    document.getElementById('itemSlide'+currentItemIndex).style.display='none';
    document.getElementById('itemSlide'+n).style.display='block';
    currentItemIndex=n;updateNav();
}
function updateNav(){
    document.getElementById('prevBtn').disabled=currentItemIndex===0;
    document.getElementById('nextBtn').disabled=currentItemIndex===totalItems-1;
    document.getElementById('itemCounter').textContent='Item '+(currentItemIndex+1)+' of '+totalItems;
}
document.addEventListener('DOMContentLoaded',function(){updateNav();});