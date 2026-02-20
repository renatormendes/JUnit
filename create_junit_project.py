import sublime
import sublime_plugin
import os
import urllib.request
import threading
import json
from datetime import datetime

class CreateJunitProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        default_path = os.path.expanduser("~") + os.sep
        self.window.show_input_panel("Caminho do novo projeto JUnit5:", default_path, self.on_selected, None, None)

    def on_selected(self, root_path):
        if not root_path or not os.path.isabs(root_path):
            sublime.error_message("Erro: Digite um caminho absoluto válido.")
            return

        project_name = os.path.basename(root_path.rstrip(os.sep))
        
        # 1. SETUP COM BUILD SYSTEM INTELIGENTE
        log_content = self.setup_project(root_path, project_name)
        
        # 2. CONFIGURAR INTERFACE
        data = self.window.project_data() or {"folders": []}
        data["folders"].append({"path": root_path})
        self.window.set_project_data(data)
        self.window.set_sidebar_visible(True)

        # 3. ABRIR ARQUIVOS
        summary_path = os.path.join(root_path, "RESUMO_PROJETO.txt")
        app_java_path = os.path.join(root_path, "src", "app", "App.java")
        
        try:
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(log_content)
            self.window.open_file(summary_path)
            self.window.open_file(app_java_path)
        except Exception as e:
            print(f"Erro: {e}")

        # 4. DOWNLOAD JUNIT 1.10.0
        jar_url = "https://repo1.maven.org"
        jar_path = os.path.join(root_path, "lib", "junit-platform-console-standalone-1.10.0.jar")
        threading.Thread(target=self.download_jar, args=(jar_url, jar_path, summary_path)).start()

    def setup_project(self, root, name):
        log = f"PROJETO: {name} | AUTO-SCAN & CORES ATIVADAS\n" + "="*40 + "\n"
        try:
            for d in ['bin', 'lib', 'src/app', 'test']:
                os.makedirs(os.path.join(root, d), exist_ok=True)

            # COMANDO MÁGICO: $(find src test -name "*.java") varre todas as subpastas
            shell_cmd = (
                "rm -rf bin && mkdir bin && "
                "javac -d bin -cp \"lib/*:bin\" $(find src test -name \"*.java\") && "
                "JAR_FILE=$(ls lib/junit-platform-console-standalone-*.jar | head -n 1) && "
                "if [ -z \"$JAR_FILE\" ]; then echo '❌ Erro: JAR não encontrado em /lib'; exit 1; fi && "
                "java -jar \"$JAR_FILE\" execute --class-path bin --scan-class-path --details-theme=unicode"
            )

            # Injeta o Build System no arquivo de projeto
            project_file = os.path.join(root, f"{name}.sublime-project")
            p_data = {
                "folders": [{"path": ".", "folder_exclude": ["bin"]}],
                "build_systems": [{
                    "name": "JUnit5 Auto-Version Runner",
                    "shell_cmd": shell_cmd,
                    "target": "ansi_color_build", # ESTA LINHA ATIVA AS CORES
                    "syntax": "Packages/ANSIescape/ANSI.sublime-syntax", # SINTAXE DE CORES
                    "working_dir": "$project_path"
                }]
            }
            with open(project_file, "w", encoding="utf-8") as f:
                f.write(json.dumps(p_data, indent=4))

            # Templates
            with open(os.path.join(root, "src/app/App.java"), "w") as f:
                f.write("package app;\npublic class App { public int somar(int a, int b) { return a+b; } }")
            with open(os.path.join(root, "test/AppTest.java"), "w") as f:
                f.write("import org.junit.jupiter.api.Test;\nimport static org.junit.jupiter.api.Assertions.*;\nimport app.App;\nclass AppTest {\n @Test void testSomar() {\n  assertEquals(2, new App().somar(1,1));\n }\n}")
            
            log += "[OK] Estrutura, Suporte a ANSI e Auto-Scanner configurados.\n"
        except Exception as e:
            log += f"[ERRO]: {e}\n"
        return log

    def download_jar(self, url, dest, log_path):
        try:
            urllib.request.urlretrieve(url, dest)
            sublime.status_message("✅ JUnit baixado!")
        except:
            sublime.error_message("Erro no download do JAR.")
