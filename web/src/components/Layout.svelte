<script>
  export let currentPage;
  let navOpen = false;

  function togglenav(){
    navOpen = !navOpen;
  }

  let pages=[
    {
      slug: "/", name: "Main Panel"
    },
    {
      slug: "/transfer/", name: "Transfer"
    },
    {
      slug: "/account/", name: "User Management"
    },
  ]
</script>

<nav class="navbar navbar-expand-lg navbar-light navbar-95 ">
        <a class="navbar-brand" href="/">
            <img src="assets/icons/computer-3.png" alt="Logo"> SecureBank</a>
        <button on:click={togglenav} 
          class="navbar-toggler" type="button" aria-controls="navbar-dropdown"
          aria-expanded={navOpen} aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse {navOpen && 'show'}" id="navbar-dropdown" >
            <ul class="navbar-nav" style="align-items: end; padding: .5rem" >
              {#each pages as page}
                <li class="nav-item {page.slug==currentPage && 'active'}">
                    <a class="nav-link" href={page.slug}>{page.name}
                    {#if page.slug==currentPage}
                      <span class="sr-only">(current)</span>
                    {/if}
                    </a>
                </li>
              {/each}
            </ul>
        </div>
</nav>
<main>
<slot />
</main>

