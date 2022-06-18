# Svelte + Vite web frontend

## development

- open a terminal in the same path as this README

- install the dependencies `npm install`

- start the development server `npm run dev`

In development mode, the frontend code will make api calls to `http://localhost:8080/api`.
To start the api server follow the [documentation](../api/README.md) in `/api`

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).

## production

To produce a production ready bundle, run `npm run build`

In production mode, the frontend will make api calls using a relative path `/api`.
This means that the api server should be located on the same domain as the frontend server.
If you use the provided dockerfiles for production environment (either from the production
docker-compose or the kubernetes build pipeline) this is already taken care of.
