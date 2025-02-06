# dsg
Data Site Generator

## create a new dsg project

After installing dsg, run the following command to create a project
```bash
dsg init project_name
```

This will create a directory with your project name. Inside your project directory, you will find the 
following:
- `pages` directory - The markdown files that make up your site. The `index.md` file is your home page.
- `sql` directory - SQL files that retrieve the data to display on the site
- `dsg.yml` file - Config file for the dsg project

## developing with dsg


## build and deploy

To create a build of your site, run the following command:
```bash
dsg build
```

This will create a `dist` directory that contains the static HTML, CSS and JavaScript files that can be deployed. 
You can deploy this as you would any static site (e.g. GitHub pages).
