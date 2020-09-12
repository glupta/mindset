<template>
  <div class="web-navbar-signedin-alert">
    <div class="left-side">
      <div class="logo"></div>
      <img class="mindset" src="https://static.overlay-tech.com/assets/33c808c7-df2a-42bb-b6a6-aa6f8fabc6ec.png"/>
    </div>
    <div class="right-side">
      <div class="verticals">
        <div class="howto">
          <p class="how-to">HOW TO</p>
        </div>
        <div class="meditate101">
          <p class="how-to">MEDITATE 101</p>
        </div>
        <div class="schedule">
          <p class="how-to">SCHEDULE</p>
        </div>
      </div>
      <SignInUserAlert class="logo-logo-28x48"></SignInUserAlert>
    </div>
  </div>
</template>

<script>
import SignInUserAlert from '@/components/SignInUserAlert';
export default {
  name: "WebNavBarSignedInAlert",
  components: { 
    SignInUserAlert
  }
};
</script>

<style scoped>
.web-navbar-signedin-alert {
  padding: 12px 44px 12px 67px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.logo-logo-28x48 {
}
.verticals {
  margin-right: 32px;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.howto {
  margin-right: 8px;
  padding: 6px 32px 7px 33px;
  display: flex;
  align-items: flex-start;
}
.how-to {
  font-family: "Source Sans Pro";
  font-size: 18px;
  font-weight: 400;
  line-height: 27px;
  color: rgba(66, 62, 61, 1);
  text-align: center;
  text-transform: uppercase;
  opacity: 0.4;
  letter-spacing: 1px;
}
.meditate101 {
  margin-right: 8px;
  padding: 6px 6px 7px 8px;
  display: flex;
  align-items: flex-start;
}
.schedule {
  padding: 6px 21px 7px 22px;
  display: flex;
  align-items: flex-start;
}
.left-side {
  display: flex;
  flex-direction: row;
}
.right-side {
  display: flex;
  flex-direction: row;
}

.rectangle {
  width: 46px;
  height: 46px;
  background-color: rgba(216, 216, 216, 1);
  margin-right: 8px;
  border: 1px solid rgba(151, 151, 151, 1);
}
.mindset {
  width: 204px;
  height: 32px;
  margin-top: 8px;
  /*margin-right: 375px;*/
}
.logo {
  width: 28px;
  height: 48px;
  margin-right: 18px;
  background-image: url("https://static.overlay-tech.com/assets/1485645f-f70c-4f26-96bd-12fa5a650103.png");
}
</style>