import sublime
import sublime_plugin
import os
import subprocess

class GenerateExecutableJarCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self.window.folders()
        if not folders: return
        root = folders[0]
        
        # Configurações
        bin_dir = os.path.join(root, "bin")
        src_dir = os.path.join(root, "src")
        out_dir = os.path.join(root, "out")
        manifest_path = os.path.join(root, "manifest.mf")
        jar_name = os.path.basename(root) + ".jar"
        jar_path = os.path.join(out_dir, jar_name)

        # 1. Criar pasta de saída
        os.makedirs(out_dir, exist_ok=True)

        # 2. Criar Manifest (Aponta para app.App se houver um main lá)
        with open(manifest_path, "w") as f:
            f.write("Manifest-Version: 1.0\n")
            f.write("Main-Class: app.App\n\n")

        # 3. Comando de Build e Empacotamento (Linux)
        # Compila -> Copia Manifest -> Gera JAR
        cmd = (
            f"javac -d {bin_dir} $(find {src_dir} -name '*.java') && "
            f"jar cvfm {jar_path} {manifest_path} -C {bin_dir} ."
        )

        sublime.status_message("📦 Gerando JAR executável...")
        
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=root)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                sublime.message_dialog(f"✅ JAR Gerado com sucesso!\n\nLocal: out/{jar_name}\n\nPara rodar: java -jar out/{jar_name}")
            else:
                sublime.error_message(f"❌ Erro ao gerar JAR:\n{stderr.decode('utf-8')}")
        except Exception as e:
            sublime.error_message(f"Erro: {e}")
