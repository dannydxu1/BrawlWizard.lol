<script>
  import { onMount } from "svelte";
  let brawlerData = [];
  let loading = true;
  let error = null;

  // Fetch data when the component mounts
  onMount(async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/brawler_data");
      if (!response.ok) {
        throw new Error("Failed to fetch brawler data");
      }
      brawlerData = await response.json();

      // Append image path to each brawler data
      brawlerData = brawlerData.map((brawler) => {
        const formattedId = brawler.brawler_id.replace(/\s+/g, "_");
        return {
          ...brawler,
          image: `images/Brawler_Skin-Default/${formattedId}_Skin-Default.webp`,
          usage_rate: brawler.usage_rate.toFixed(2) + "%",
          win_rate: (brawler.win_rate * 100).toFixed(2) + "%",
        };
      });
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  });
</script>

<div class="rankings-container">
  {#if loading}
    <div class="loading">Fetching brawler data, please wait...</div>
  {:else if error}
    <div class="error">Error: {error}</div>
  {:else}
    <div class="brawler-grid">
      {#each brawlerData as brawler}
        <div class="brawler-card">
          <img
            src={brawler.image}
            alt={brawler.brawler_id}
            class="brawler-image"
          />
          <h3>{brawler.brawler_id}</h3>
          <p>
            Rank: {brawler.rank}
          </p>
          <p>Win Rate: {brawler.win_rate}</p>
          <p>Usage Rate: {brawler.usage_rate}</p>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .rankings-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .loading,
  .error {
    font-size: 1.5em;
    text-align: center;
    margin-top: 20px;
  }

  .brawler-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
  }

  .brawler-card {
    background-color: #283593;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }

  .brawler-card h3 {
    color: #ffeb3b;
    margin-top: 10px;
  }

  .brawler-card p {
    margin: 5px 0;
    color: #fff; /* Set the text color to white */
  }

  .brawler-image {
    width: 100px; /* Normalized width */
    height: 100px; /* Normalized height */
    object-fit: cover; /* Ensures the image covers the box without stretching */
    object-position: top; /* Prioritizes the top part of the image */
    border-radius: 5px;
  }
</style>
