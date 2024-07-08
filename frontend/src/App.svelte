<script>
  import Router, { location, link } from "svelte-spa-router";
  import Home from "./Home.svelte";
  import About from "./About.svelte";
  import Profile from "./Profile.svelte";
  import BrawlerRankings from "./BrawlerRankings.svelte";
</script>

<nav>
  <a href="/">Home</a>
  <a href="/#/about">About</a>
  <a href="/#/brawler-rankings">BrawlerRankings</a>
</nav>

<Router
  routes={{
    "/": Home,
    "/about": About,
    "/brawler-rankings": BrawlerRankings,
    "/profile/:profileID": Profile,
  }}
/>

<hr />
/#{$location}
