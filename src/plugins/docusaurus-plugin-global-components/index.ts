// This is a Docusaurus plugin to add the global chatbot component
import { LoadContext, Plugin } from '@docusaurus/types';
import path from 'path';

export default function pluginGoogleTagManager(
  context: LoadContext,
): Plugin<void> {
  return {
    name: 'docusaurus-plugin-global-components',

    getClientModules() {
      return [path.resolve(__dirname, '../components/GlobalChatbot')];
    },
  };
}