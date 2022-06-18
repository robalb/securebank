<script>
  import Counter from '../components/Counter.svelte'
  import Layout from '../components/Layout.svelte'
</script>

<Layout currentPage={"/"}>
  <h1>Hello world!</h1>

  <Counter />

  <p>
    Visit <a href="https://svelte.dev">svelte.dev</a> to learn how to build Svelte
    apps.
  </p>

  <p>
    Check out <a href="https://github.com/sveltejs/kit#readme">SvelteKit</a> for
    the officially supported framework, also powered by Vite!
  </p>
</Layout>

<style>

</style>
