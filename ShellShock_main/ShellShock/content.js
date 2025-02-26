const urls = document.querySelectorAll("a");

function inject_url(){
  urls.forEach(function(anchor){
    anchor.href = "http://127.0.0.1:5000/";
  });
}

inject_url()
const observer = new MutationObserver(() => {
  inject_url()

});


observer.observe(document.body, { childList: true, subtree: true });
