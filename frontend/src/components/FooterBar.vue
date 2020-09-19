<template>
  <div class="footerbar">
    <div class="foot-left">
      <img alt="logo-logo-40x40" class="logo-logo-40x40"
      src="https://static.overlay-tech.com/assets/79194d3f-6d5d-4980-a1f6-2851afaaacfd.png"/>
      <img alt="logo-text-254x40" class="logo-text-457x72" src="https://static.overlay-tech.com/assets/48578421-63ec-4935-a66f-ccf515589395.png"/>
    </div>
    <div class="foot-right">
      <p class="about">ABOUT</p>
      <p class="contact">CONTACT</p>
      <p class="the-science">THE SCIENCE</p>
      <p class="faq--support">FAQ & SUPPORT</p>
      <p class="terms-of-service">TERMS OF SERVICE</p>
      <p class="privacy-policy">PRIVACY POLICY</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "FooterBar"
};
</script>

<style scoped>
.footerbar {
  padding: 8px 64px 8px 64px;
  width: 100%;
  box-shadow: 0px -1px 3px 0px rgba(103, 68, 58, 0.1);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background: linear-gradient(
    91deg,
    rgba(239, 235, 220, 1) 42%,
    rgba(191, 180, 139, 1) 161%
  );
}
.foot-left {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}
.foot-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
}
.logo-logo-40x40 {
  margin-right: 8px;
  width: 40px;
  height: 40px;
}
.logo-text-457x72 {
  /*margin-right: 338px;*/
  width: 254px;
  height: 40px;
}
.about {
  font-family: "Source Sans Pro";
  font-size: 12px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  letter-spacing: 1px;
  margin-right: 48px;
}
.contact {
  font-family: "Source Sans Pro";
  font-size: 12px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  margin-right: 48px;
  letter-spacing: 1px;
}
.the-science {
  font-family: "Source Sans Pro";
  font-size: 12px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  margin-right: 48px;
  letter-spacing: 1px;
}
.faq--support {
  font-family: "Source Sans Pro";
  font-size: 12px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  margin-right: 48px;
  letter-spacing: 1px;
}
.terms-of-service {
  font-family: "Source Sans Pro";
  font-size: 12px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  margin-right: 48px;
  letter-spacing: 1px;
}
.privacy-policy {
  font-family: "Source Sans Pro";
  font-size: 12px;
  font-weight: 400;
  line-height: 24px;
  color: rgba(66, 62, 61, 1);
  text-align: right;
  letter-spacing: 1px;
}
</style>