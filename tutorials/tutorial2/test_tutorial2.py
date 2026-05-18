import unittest
from pathlib import Path
from maltoolbox.model import Model
from maltoolbox.language import LanguageGraph

current_dir = Path(__file__).parent


class TestTutorial2(unittest.TestCase):

    def test_mal_example(self):
        language_path = str(current_dir) + "/resources/org.mal-lang.coreLang-1.0.0.mar"
        language_graph = LanguageGraph.from_mar_archive(language_path)
        model = Model("Tutorial2 Model", language_graph)

        # Add Hardware
        hw_comp_1 = model.add_asset("Hardware", name="Computer")
        hw_server_1 = model.add_asset("Hardware", name="Server")

        # Add Software
        sw_win_1 = model.add_asset("Application", name="Windows 11")
        sw_win_server = model.add_asset("Application", name="Windows Server")

        # Add relations between hardware and software
        hw_comp_1.add_associated_assets("sysExecutedApps", {sw_win_1})
        hw_server_1.add_associated_assets("sysExecutedApps", {sw_win_server})

        # Software applications
        app_docker = model.add_asset("Application", name="Docker")
        app_ssh = model.add_asset("Application", name="SSH server")

        # Add relations between application and application
        sw_win_1.add_associated_assets("appExecutedApps", {app_docker})
        sw_win_server.add_associated_assets("appExecutedApps", {app_ssh})

        # Add connection rules
        cr_docker_1 = model.add_asset("ConnectionRule", name="docker:4443")
        cr_ssh_1 = model.add_asset("ConnectionRule", name="ssh:22")

        # Add connection rules for docker
        app_docker.add_associated_assets("ingoingAppConnections", {cr_docker_1})
        app_ssh.add_associated_assets("appConnections", {cr_ssh_1})

        # Add simple network
        nw_1 = model.add_asset("Network", name="Network")

        # Connect to network
        nw_1.add_associated_assets("netConnections", {cr_docker_1})
        nw_1.add_associated_assets("netConnections", {cr_ssh_1})

        # Add vulnerabilities
        vuln_web = model.add_asset("SoftwareVulnerability", name="Web exploit")
        vuln_os = model.add_asset("SoftwareVulnerability", name="OS exploit")

        # Add connection between vulns and apps
        vuln_web.add_associated_assets("application", {app_docker})
        vuln_os.add_associated_assets("application", {sw_win_server})

        # Add identities to assets
        id_admin = model.add_asset("Identity", name="admin_identity")
        id_web_app = model.add_asset("Identity", name="web_app_identity")

        # Add credentials to assets
        cred_admin = model.add_asset("Credentials", name="admin_credentials")
        cred_web_app = model.add_asset("Credentials", name="web_app_credentials")

        # Add user
        user_josh = model.add_asset("User", name="User 1")

        # Add associations between user, credentials and identitites
        user_josh.add_associated_assets("userIds", {id_admin, id_web_app})
        id_admin.add_associated_assets("credentials", {cred_admin})
        id_web_app.add_associated_assets("credentials", {cred_web_app})

        # Add associations from user/identity to assets
        # Hardware access
        user_josh.add_associated_assets("hardwareSystems", {hw_comp_1})
        # Admin access to OS
        id_admin.add_associated_assets("highPrivApps", {sw_win_1})
        # User access to webservice
        id_web_app.add_associated_assets("lowPrivApps", {app_docker})

        # render_model(model)
