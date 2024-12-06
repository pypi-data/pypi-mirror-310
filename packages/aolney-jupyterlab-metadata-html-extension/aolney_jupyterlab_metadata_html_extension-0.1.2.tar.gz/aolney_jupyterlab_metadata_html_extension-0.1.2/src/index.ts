import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { 
  INotebookTracker, 
  NotebookPanel 
} from "@jupyterlab/notebook";

import {
  IWidgetTracker
} from '@jupyterlab/apputils';

import {
  MarkdownCell
} from '@jupyterlab/cells';

/**
 * Inject html. Note this only happens if the notebook changes
 * @param notebook 
 */
function injectHtml( notebook: NotebookPanel): void {
  console.log("html injection")
  //check each cell for injection
  let cells = notebook.content.widgets
  for( let i = 0; i < cells.length - 1; i++)
  {
    let cell = cells[i]
    //only inject markdown cells
    if( cell.model.type == "markdown" )
    {
      let markdownCell:MarkdownCell = cell as MarkdownCell
      let html:string = markdownCell.model.getMetadata("html") ?? null
      //only inject if we have html metadata to inject
      if( html !== null)
      {
        //navigate in the DOM to align our HTML with the rendered markdown; likely fragile to future JLab changes
        // let inputWrapper = markdownCell.node.children[1] 
        // let inputArea = inputWrapper.children[1] 
        // let target = inputArea.children[2] 
        let target = markdownCell.node
        //check for previous injection to avoid duplication; the last attribute would have a classlist that includes "metadata-html"
        let lastChildElement = target.lastElementChild
        if(lastChildElement?.classList == null ||  !lastChildElement?.classList.contains("metadata-html") )
        {
          //we have no existing injected element, so proceed
          target.insertAdjacentHTML("beforeend", html)
        }
      }
    }   
  }
}

/**
 * We catch a notebook changed because only at this point is the page set up enough to inject html
 * @param this 
 * @param sender 
 * @param args 
 * @returns 
 */
export function onNotebookChanged(this: any, sender: IWidgetTracker<NotebookPanel>, args: NotebookPanel | null): boolean{
  console.log("notebook changed");
  let notebookPanelOption = sender.currentWidget
  if( notebookPanelOption !== null)
  {
    let notebookPanel : NotebookPanel = notebookPanelOption
    console.log('@aolney/jupyterlab-metadata-html-extension: notebook changed to ' + notebookPanel.context.path);
    notebookPanel.revealed.then<void>(
      ():void => {
        injectHtml(notebookPanel)
      }
    )
  }
  return true;
}

/**
 * Initialization data for the @aolney/jupyterlab-metadata-html-extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@aolney/jupyterlab-metadata-html-extension:plugin',
  description: 'A JupyterLab extension that uses cell metadata to define html that is injected into markdown cells.',
  autoStart: true,
  requires: [INotebookTracker],
  activate: (app: JupyterFrontEnd, notebooks: INotebookTracker) => {
    console.log('JupyterLab extension @aolney/jupyterlab-metadata-html-extension is activated!');
    notebooks.currentChanged.connect(onNotebookChanged, null);
  }
};

export default plugin;
