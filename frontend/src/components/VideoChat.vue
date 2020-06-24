<!--template>
  <div>
    {{ room_url }}
  </div>
</template-->

<script>
export default {
  name: 'VideoChat',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
    }
  },
  props: [
    'roomReady',
    'room_url'
  ],
  // watch: {
  //   this.JoinVideoCall(this.room_url);
  // },
  methods: {

    JoinVideoCall(room_url) {

      console.log("room name url:",room_url);

      let dailycoScript = document.createElement('script');
      dailycoScript.addEventListener("load", function(event) {
        window.callFrame = window.DailyIframe.createFrame();
        callFrame.join({ url: room_url});
        var elem = document.querySelector('iframe');
        elem.style.width= "375px";
        elem.style.height = "750px";
        elem.style.right= "0em";
        elem.style.bottom= "0em";
      });
      dailycoScript.setAttribute('src', 'https://unpkg.com/@daily-co/daily-js/dist/daily-iframe.js');
      document.head.appendChild(dailycoScript);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<!--style scoped>
.timer {
  float:left;
}
</style-->
