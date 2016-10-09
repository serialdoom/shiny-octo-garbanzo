# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  #config.vm.box = "ubuntu/xenial64"
  config.vm.network "public_network", bridge: ENV.fetch('VAGRANT_NETWORK_IFACE', 'em1')
  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=777", "fmode=666"]
  config.vm.synced_folder "./downloads/sonarr/backups/", "/home/vagrant/sonarr/Backups", mount_options: ["dmode=777", "fmode=666"]

  config.vm.provision :shell, inline: <<-SHELL
    sudo apt-get install -y python
  SHELL
  config.vm.provision :ansible do |ansible|
      ansible.playbook = 'setup.yml'
      ansible.sudo = true
      ansible.groups = {
          'all' => ['default'],
          'all:vars' => {
              'docker_py_version' => '1.9.0',
          }
      }
  end
end
