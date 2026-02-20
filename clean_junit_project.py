import sublime
import sublime_plugin
import os
import shutil

class CleanJunitProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Pega a pasta raiz do projeto aberto
        folders = self.window.folders()
        if not folders:
            sublime.status_message("❌ Nenhum projeto aberto para limpar.")
            return
        
        root_path = folders[0]
        bin_path = os.path.join(root_path, "bin")
        log_path = os.path.join(root_path, "RESUMO_PROJETO.txt")
        
        try:
            # Remove a pasta bin e seu conteúdo
            if os.path.exists(bin_path):
                shutil.rmtree(bin_path)
                os.makedirs(bin_path) # Recria vazia
            
            # Opcional: Remove o log de resumo se desejar
            if os.path.exists(log_path):
                os.remove(log_path)

            sublime.message_dialog("Limpeza concluída!\n\nPastas 'bin' e logs foram removidos.")
            sublime.status_message("✅ Projeto limpo com sucesso.")
            
        except Exception as e:
            sublime.error_message(f"Erro ao limpar projeto: {e}")
