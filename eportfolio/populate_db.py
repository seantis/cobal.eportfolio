# -*- coding: utf-8 -*-

import datetime
import os
import transaction

from paste.deploy import appconfig
from paste.script.command import Command

from eportfolio.models import initialize_sql
from eportfolio.models import DBSession
from eportfolio.models import MetaCompetence
from eportfolio.models import Competence
from eportfolio.models import Project
from eportfolio.models import IndicatorSet
from eportfolio.models import Indicator
from eportfolio.models import Teacher
from eportfolio.models import Student
from eportfolio.models import JournalEntry
from eportfolio.models import Comment

class PopulateDBCommand(Command):
    
    # Parser configuration
    summary = "--NO SUMMARY--"
    usage = "--NO USAGE--"
    group_name = "eportfolio"
    parser = Command.standard_parser(verbose=False)
    
    def command(self):
        self._setup_db()
        self._populate_db()
        transaction.commit()
    
    def _setup_db(self):
        config_uri = 'config:%s' % self.args[0]
        here_dir = os.getcwd()
        settings = appconfig(config_uri, name='eportfolio', relative_to=here_dir)
        db_string = settings.get('db_string')
        if db_string is None:
            raise ValueError("No 'db_string' value in application configuration.")
        initialize_sql(db_string)
    
    def _populate_db(self):
        
        session = DBSession()
        
        # Add meta competences
        media = MetaCompetence(title=u'Media')
        technical = MetaCompetence(title=u'Technical')
        language = MetaCompetence(title=u'Language')
        maths = MetaCompetence(title=u'Math')
        key = MetaCompetence(title=u'Key')
        
        session.add_all([media, technical, language, maths, key])
        
        # Add a project
        concepts_ict = Project(title=u'Concepts of Information and Communication Technology (ICT)')
        session.add(concepts_ict)
        
        # Add competence hardware to the project
        hardware = Competence(title=u'Hardware')
        hardware.meta_competence = technical
        hardware.description = u'Understand what hardware is, know about factors that affect computer performance and know about peripheral devices.'
        concepts_ict.competences.append(hardware)
        # Indicator set concepts
        hardware_concepts = IndicatorSet(title=u'Concepts')
        hardware_concepts.competence = hardware
        understand_term = Indicator(
                                title=u'Understand the Term Hardware',
                                description=u'Understand the term hardware.',
                                sort_order=0)
        hardware_concepts.indicators.append(understand_term)
        understand_pc = Indicator(
                                title=u'Understand what a Personal Computer is',
                                description=u'Understand what a personal computer is. Distinguish between desktop, laptop (notebook), tablet PC in terms of typical users.',
                                sort_order=1)
        hardware_concepts.indicators.append(understand_pc)
        identify_devices = Indicator(
                                title=u'Identify Handheld Portable Digital Devices',
                                description=u'Identify common handheld portable digital devices like: personal digital assistant (PDA), mobile phone, smartphone, multimedia player and know their main features.',
                                sort_order=2)
        hardware_concepts.indicators.append(identify_devices)
        know_main_parts = Indicator(
                                title=u'Know the Main Parts of a Computer',
                                description=u'Know the main parts of a computer like: central processing unit (CPU), types of memory, hard disk, common input and output devices.',
                                sort_order=3)
        hardware_concepts.indicators.append(know_main_parts)
        identify_output_input = Indicator(
                                title=u'Identify Common Input/Output Ports',
                                description=u'Identify common input/output ports like: USB, serial, parallel, network port, FireWire.',
                                sort_order=4)
        hardware_concepts.indicators.append(identify_output_input)
        # Indicator set Computer Performance
        computer_performance = IndicatorSet(title=u'Computer Performance')
        computer_performance.competence = hardware
        impact_performance = Indicator(
                                title=u'Know some of the factors that impact on a computer’s performance',
                                description=u'Know some of the factors that impact on a computer’s performance like: CPU speed, RAM size, graphics card processor and memory, the number of applications running.',
                                sort_order=0)
        computer_performance.indicators.append(impact_performance)
        operating_frequency = Indicator(
                                title=u'Know speed measurements (operating frequency) of the CPU',
                                description=u'Know that the speed (operating frequency) of the CPU is measured in megahertz (MHz) or gigahertz (GHz).',
                                sort_order=1)
        computer_performance.indicators.append(operating_frequency)
        # Indicator set Memory and Storage
        memory_storage = IndicatorSet(title=u'Memory and Storage')
        memory_storage.competence = hardware
        know_memory = Indicator(
                                title=u'Know what computer memory is',
                                description=u'Know what computer memory is: RAM (random-access memory), ROM (readonly memory) and distinguish between them.',
                                sort_order=0)
        memory_storage.indicators.append(know_memory)
        storage_capacity = Indicator(
                                title=u'Know storage capacity measurements',
                                description=u'Know storage capacity measurements: bit, byte, KB, MB, GB, TB.',
                                sort_order=1)
        memory_storage.indicators.append(storage_capacity)
        storage_media = Indicator(
                                title=u'Know the main types of storage media',
                                description=u'Know the main types of storage media like: internal hard disk, external hard disk, network drive, CD, DVD, USB flash drive, memory card, online file storage.',
                                sort_order=2)
        memory_storage.indicators.append(storage_media)
        # Indicator set Input, Output Devices
        input_output = IndicatorSet(title=u'Input, Output Devices')
        input_output.competence = hardware
        identify_input = Indicator(
                                title=u'Identify some of the main input devices',
                                description=u'Identify some of the main input devices like: mouse, keyboard, trackball, scanner, touchpad, stylus, joystick, web camera (webcam), digital camera, microphone.',
                                sort_order=1)
        input_output.indicators.append(identify_input)
        identify_output = Indicator(
                                title=u'Know some of the main output devices',
                                description=u'Know some of the main output devices like: screens/monitors, printers, speakers, headphones.',
                                sort_order=2)
        input_output.indicators.append(identify_output)
        dual_devices = Indicator(
                                title=u'Understand some devices are both input and output devices',
                                description=u'Understand some devices are both input and output devices like: touchscreens.',
                                sort_order=3)
        input_output.indicators.append(dual_devices)
        
        # Add competence software to the project
        software = Competence(title=u'Software')
        hardware.meta_competence = technical
        software.description = u'Understand what software is and give examples of common applications software and operating system software.'
        concepts_ict.competences.append(software)
        # Indicator set concepts
        software_concepts = IndicatorSet(title=u'Concepts')
        software_concepts.competence = software
        understand_term_software = Indicator(
                                title=u'Understand the term software.',
                                description=u'Understand the term software',
                                sort_order=0)
        software_concepts.indicators.append(understand_term_software)
        understand_os = Indicator(
                                title=u'Understand what an operating system is',
                                description=u'Understand what an operating system is and name some common operating systems.',
                                sort_order=1)
        software_concepts.indicators.append(understand_os)
        common_software = Indicator(
                                title=u'Identify and know the uses of some common software applications',
                                description=u'Identify and know the uses of some common software applications: word processing, spreadsheet, database, presentation, e-mail, web browsing, photo editing, computer games.',
                                sort_order=2)
        software_concepts.indicators.append(common_software)
        distinguish_os = Indicator(
                                title=u'Distinguish between operating systems software and applications software.',
                                description=u'Distinguish between operating systems software and applications software.',
                                sort_order=3)
        software_concepts.indicators.append(distinguish_os)
        enhance_accessibility = Indicator(
                                title=u'Know some options available for enhancing accessibility',
                                description=u'Know some options available for enhancing accessibility like: voice recognition software, screen reader, screen magnifier, on-screen keyboard.',
                                sort_order=4)
        software_concepts.indicators.append(enhance_accessibility)
        # Add competence network to the project
        network = Competence(title=u'Network')
        network.meta_competence = technical
        network.description = u'Understand how information networks are used within computing, and be aware of the different options to connect to the Internet.'
        concepts_ict.competences.append(network)
        # Indicator set network types
        network_types = IndicatorSet(title=u'Network Types')
        network_types.competence = network
        understand_terms_LAN_WLAN_WAN = Indicator(
                                title=u'Understand the terms LAN, WLAN, WAN.',
                                description=u'Understand the terms local area network (LAN), wireless local area network (WLAN), wide area network (WAN).',
                                sort_order=0)
        network_types.indicators.append(understand_terms_LAN_WLAN_WAN)
        understand_term_client = Indicator(
                                title=u'Understand the term client/server',
                                description=u'Understand the term client/server',
                                sort_order=1)
        network_types.indicators.append(understand_term_client)
        understand_internet = Indicator(
                                title=u'Understand what the Internet is and know some of its main uses.',
                                description=u'Understand what the Internet is and know some of its main uses.',
                                sort_order=2)
        network_types.indicators.append(understand_internet)
        understand_intranet_extranet = Indicator(
                                title=u'Understand what an intranet, extranet is.',
                                description=u'Understand what an intranet, extranet is.',
                                sort_order=3)
        network_types.indicators.append(understand_intranet_extranet)
        # Indicator set data transfer
        data_transfer = IndicatorSet(title=u'Data Transfer')
        data_transfer.competence = network
        understand_download_upload = Indicator(
                                title=u'Understand the concepts of downloading and uploading',
                                description=u'Understand the concepts of downloading from, uploading to a network.',
                                sort_order=0)
        data_transfer.indicators.append(understand_download_upload)
        understand_transfer_rate = Indicator(
                                title=u'Understand what transfer rate means and its measurement.',
                                description=u'Understand what transfer rate means. Understand how it is measured: bits per second (bps), kilobits per second (kbps), megabits per second (mbps).',
                                sort_order=1)
        data_transfer.indicators.append(understand_transfer_rate)
        internet_connectionservices = Indicator(
                                title=u'Know about different Internet connection services.',
                                description=u'Know about different Internet connection services: dial-up, broadband.',
                                sort_order=2)
        data_transfer.indicators.append(internet_connectionservices)
        internet_connectionoptions = Indicator(
                                title=u'Know about different options for connecting to the Internet.',
                                description=u'Know about different options for connecting to the Internet like: phone line, mobile phone, cable, wireless, satellite.',
                                sort_order=3)
        data_transfer.indicators.append(internet_connectionoptions)
        broadband_characteristics = Indicator(
                                title=u'Understand some of the characteristics of broadband',
                                description=u'Understand some of the characteristics of broadband: always on, typically a flat fee, high speed, higher risk of intruder attack.',
                                sort_order=4)
        data_transfer.indicators.append(broadband_characteristics)
        # Add competence ICT in everyday life to the project
        ict_in_everyday_life = Competence(title=u'ICT in everyday life')
        ict_in_everyday_life.meta_competence = technical
        ict_in_everyday_life.description = u'Understand what Information and Communication Technology (ICT) is and give examples of its practical applications in everyday life.Understand health and safety and environmental issues in relation to using computers.'
        concepts_ict.competences.append(ict_in_everyday_life)
        # Indicator set Electronic world
        electronic_world = IndicatorSet(title=u'Electronic World')
        electronic_world.competence = ict_in_everyday_life
        understand_term_ict= Indicator(
                              title=u'Understand the term Information and Communication Technology (ICT)',
                              description=u'Understand the term Information and Communication Technology (ICT)',
                              sort_order=0)
        electronic_world.indicators.append(understand_term_ict)
        consumers_internet_services = Indicator(
                              title=u'Know about different Internet services for consumers.',
                              description=u'Know about different Internet services for consumers like: e-commerce, e- banking, e-government.',
                              sort_order=1)
        electronic_world.indicators.append(consumers_internet_services)
        elearning = Indicator(
                              title=u'Understand the term e-learning.',
                              description=u'Understand the term e-learning. Know some of its features like: flexible learning time, flexible learning location, multimedia learning experience, cost effectiveness.',
                              sort_order=2)
        electronic_world.indicators.append(elearning)
        teleworking = Indicator(
                              title=u'Understand the term teleworking.',
                              description=u'Understand the term teleworking. Know some of the advantages of teleworking like: reduced or no commuting time, greater ability to focus on one task, flexible schedules, reduced company space requirements. Know some disadvantages of teleworking like: lack of human contact, less emphasis on teamwork.',
                              sort_order=3)  
        electronic_world.indicators.append(teleworking)    
        # Indicator set communication
        communication = IndicatorSet(title=u'Communication')
        communication.competence = ict_in_everyday_life
        email = Indicator(
                              title=u'Understand the term electronic mail (e-mail).',
                              description=u'Understand the term electronic mail (e-mail).',
                              sort_order=0)  
        communication.indicators.append(email)
        understand_term_im = Indicator(
                              title=u'Understand the term instant messaging (IM).',
                              description=u'Understand the term instant messaging (IM).',
                              sort_order=1)
        communication.indicators.append(understand_term_im)
        understand_term_voip = Indicator(
                              title=u'Understand the term Voice over Internet Protocol (VoIP).',
                              description=u'Understand the term Voice over Internet Protocol (VoIP).',
                              sort_order=2)
        communication.indicators.append(understand_term_voip)
        understand_rss = Indicator(   
                              title=u'Understand the term Really Simple Syndication (RSS) feed.',
                              description=u'Understand the term Really Simple Syndication (RSS) feed.',
                              sort_order=3)
        communication.indicators.append(understand_rss)
        blog = Indicator(
                              title=u'Understand the term web log (blog).',
                              description=u'Understand the term web log (blog).',
                              sort_order=4)
        communication.indicators.append(blog)
        podcast = Indicator(
                              title=u'Understand the term podcast.',
                              description=u'Understand the term podcast.',
                              sort_order=5)
        communication.indicators.append(podcast)   
        # Indicator set virtual communities
        virtual_communities = IndicatorSet(title=u'Virtual communities')
        virtual_communities.competence = ict_in_everyday_life
        concept_online_communitiy = Indicator(
                               title=u'Understand the concept of an online (virtual) community.',
                               description=u'Understand the concept of an online (virtual) community. Recognize examples like: social networking websites, Internet forums, chat rooms, online computer games.',
                               sort_order=0)
        virtual_communities.indicators.append(concept_online_communitiy)
        publish_share_content = Indicator(
                               title=u'Know ways that users can publish and share content online.',
                               description=u'Know ways that users can publish and share content online: web log (blog), podcast, photos, video and audio clips.',
                               sort_order=1)
        virtual_communities.indicators.append(publish_share_content)
        precautions = Indicator(
                               title=u'Know the importance of taking precautions when using online communities.',
                               description=u'Know the importance of taking precautions when using online communities: make your profile private, limit the amount of personal information you post, be aware that posted information is publicly available, be wary of strangers.',
                               sort_order=2)
        virtual_communities.indicators.append(precautions)
        # Indicator set Health
        health = IndicatorSet(title=u'Health')
        health.competence = ict_in_everyday_life
        ergonomics = Indicator(
                               title=u'Understand the term ergonomics',
                               description=u'Understand the term ergonomics',
                               sort_order=0)
        health.indicators.append(ergonomics)
        lightning = Indicator(
                               title=u'Recognize that lighting is a health factor in computer use.',
                               description=u'Recognize that lighting is a health factor in computer use. Be aware that use of artificial light, amount of light, direction of light are all important considerations.',
                               sort_order=1)
        health.indicators.append(lightning)
        positioning = Indicator(
                               title=u'Understand that correct positioning of the computer, desk and seat can help maintain a good posture.',
                               description=u'Understand that correct positioning of the computer, desk and seat can help maintain a good posture.',
                               sort_order=2)
        health.indicators.append(positioning)
        wellbeing = Indicator(
                               title=u'Recognize ways to help ensure a user’s wellbeing while using a computer.',
                               description=u'Recognize ways to help ensure a user’s wellbeing while using a computer like: take regular stretches, have breaks, use eye relaxation techniques.',
                               sort_order=3)
        health.indicators.append(wellbeing)
        # Indicator set Environment
        environment = IndicatorSet(title=u'Environment')
        environment.competence = ict_in_everyday_life
        recycling = Indicator(
                               title=u'Know about the option of recycling computer components, printer cartridges and paper.',
                               description=u'Know about the option of recycling computer components, printer cartridges and paper.',
                               sort_order=0)
        environment.indicators.append(recycling)
        energy_saving = Indicator(
                               title=u'Know about computer energy saving options.',
                               description=u'Know about computer energy saving options: applying settings to automatically turn off the screen/monitor, to automatically put the computer to sleep, switching off the computer.',
                               sort_order=1)
        environment.indicators.append(energy_saving)
        # Add competence Security to project
        security = Competence(title=u'Security')
        security.meta_competence = technical
        security.description = u'Recognize important security issues associated with using computers.'
        concepts_ict.competences.append(security)   
        # Indicator set Identity/Authentication
        identity = IndicatorSet(title=u'Identity/Authentication')
        identity.competence = security
        id_password = Indicator(
                               title=u' Understand that for security reasons a user name (ID) and password are needed for users to identify themselves when logging on to a computer.',
                               description=u' Understand that for security reasons a user name (ID) and password are needed for users to identify themselves when logging on to a computer.',
                               sort_order=0)
        identity.indicators.append(id_password)
        password_policies = Indicator(
                               title=u'Know about good password policies.',
                               description=u'Know about good password policies like: not sharing passwords, changing them regularly, adequate password length, adequate letter and number mix.',
                               sort_order=1)
        identity.indicators.append(password_policies)
        # Indicator set Data Security
        data_security = IndicatorSet(title=u'Data Security')
        data_security.competence = security
        backup_copy = Indicator(
                                title=u'Understand the importance of having an off-site backup copy of files.',
                                description=u'Understand the importance of having an off-site backup copy of files.',
                                sort_order=0)
        data_security.indicators.append(backup_copy)
        firewall = Indicator(
                              title=u'Understand what a firewall is.',
                              description=u'Understand what a firewall is.',
                              sort_order=1)
        data_security.indicators.append(firewall)
        data_theft = Indicator(
                              title=u'Know ways to prevent data theft.',
                              description=u'Know ways to prevent data theft like: using a user name and password, locking computer and hardware using a security cable.',
                              sort_order=2)
        data_security.indicators.append(data_theft)
        # Indicator set Viruses
        viruses = IndicatorSet(title=u'Viruses')
        viruses.competence = security
        term_virus = Indicator(
                              title=u'Understand the term computer virus.',
                              description=u'Understand the term computer virus.',
                              sort_order=0)
        viruses.indicators.append(term_virus)
        virus_enter = Indicator(
                              title=u'Be aware how viruses can enter a computer system.',
                              description=u'Be aware how viruses can enter a computer system.',
                              sort_order=1)
        viruses.indicators.append(virus_enter)
        virus_protection = Indicator(
                              title=u'Know how to protect against viruses and the importance of updating anti- virus software regularly.',
                              description=u'Know how to protect against viruses and the importance of updating anti- virus software regularly.',
                              sort_order=2)
        viruses.indicators.append(virus_protection)
        # Add competence Law to project
        law = Competence(title=u'Law')
        law.meta_competence = technical
        law.description = u'Recognize important legal issues in relation to copyright and data protection associated with using computers.'
        concepts_ict.competences.append(law)
        # Indicator set copyright
        copyright = IndicatorSet(title=u'Copyright')
        copyright.competence = law
        term_copyright = Indicator(
                              title=u'Understand the term copyright.',
                              description=u'Understand the term copyright.',
                              sort_order=0)
        copyright.indicators.append(term_copyright)
        licensed_software = Indicator(
                              title=u'Know how to recognize licensed software.',
                              description=u'Know how to recognize licensed software: by checking product ID, product registration, by viewing the software licence.',
                                          sort_order=1)
        copyright.indicators.append(licensed_software)
        enduser_license_agreement = Indicator(
                              title= u'Understand the term end-user license agreement.',
                              description=u'Understand the term end-user license agreement.',
                              sort_order=2)
        copyright.indicators.append(enduser_license_agreement)
        shareware_freeware_os = Indicator(
                              title=u'Understand the terms shareware, freeware, open source.',
                              description=u'Understand the terms shareware, freeware, open source.',
                              sort_order=3)
        copyright.indicators.append(shareware_freeware_os)
        # Indicator set Data Protection
        data_protection = IndicatorSet(title=u'Data Protection')
        data_protection.competence = law
        purpose_of_dataprotection = Indicator(
                              title=u'Identify the main purposes of data protection legislation or conventions',
                              description=u'Identify the main purposes of data protection legislation or conventions: to protect the rights of the data subject, to set out the controller.',
                              sort_order=0)
        data_protection.indicators.append(purpose_of_dataprotection)
        dataprotection_rights = Indicator(
                              title=u'Identify the main data protection rights for a data subject in your country.',
                              description=u'Identify the main data protection rights for a data subject in your country.',
                              sort_order=1)
        data_protection.indicators.append(dataprotection_rights)
        dataprotection_responsibilities = Indicator(
                              title=u'Identify the main data protection responsibilities for a data controller in your country.',
                              description=u'Identify the main data protection responsibilities for a data controller in your country.',
                              sort_order=2)
        data_protection.indicators.append(dataprotection_responsibilities)    
        
        # Add a project
        using_managingfiles = Project(title=u'Using the Computer and Managing Files')
        session.add(using_managingfiles)
        
        # Add competence operating system to the project
        operating_system = Competence(title=u'Operating system')
        operating_system.meta_competence = technical
        operating_system.description = u'Use the main features of the operating system including adjusting the main computer settings and using built-in help features.Operate effectively around the computer desktop and work effectively in a graphical user environment.'
        using_managingfiles.competences.append(operating_system)
        # Indicator set first steps
        first_steps = IndicatorSet(title=u'First Steps')
        first_steps.competence = operating_system
        start = Indicator(
                            title=u'Start the computer and log on securely using a user name and password.',
                            description=u'Start the computer and log on securely using a user name and password.',
                            sort_order=0)
        first_steps.indicators.append(start)
        restart = Indicator(
                            title=u'Restart the computer using an appropriate routine.',
                            description=u'Restart the computer using an appropriate routine.',
                            sort_order=1)
        first_steps.indicators.append(restart)
        shutdown_application = Indicator(
                            title=u'Shut down a non-responding application.',
                            description=u'Shut down a non-responding application.',
                            sort_order=2)
        first_steps.indicators.append(shutdown_application)
        shutdown_computer = Indicator(
                            title=u'Shut down the computer using an appropriate routine.',
                            description=u'Shut down the computer using an appropriate routine.',
                            sort_order=3)
        first_steps.indicators.append(shutdown_computer)
        help_functions = Indicator(
                            title=u'Use available Help functions',
                            description=u'Use available Help functions',
                            sort_order=4)
        first_steps.indicators.append(help_functions)
        # Indicator set Setup
        setup = IndicatorSet(title=u'Setup')
        setup.competence = operating_system
        basic_system_information = Indicator(
                            title=u'View the computer’s basic system information',
                            description=u'View the computer’s basic system information: operating system name and version number, installed RAM (random- access memory).',
                            sort_order=0)
        setup.indicators.append(basic_system_information)
        change_desktop_configuration = Indicator(
                            title=u'Change the computer’s desktop configuration',
                            description=u'Change the computer’s desktop configuration: date & time, volume settings, desktop display options (colour settings, desktop background, screen pixel resolution, screen saver options)',
                            sort_order=1)
        setup.indicators.append(change_desktop_configuration)
        keyboard_language = Indicator(
                            title=u'Set, add keyboard language.',
                            description=u'Set, add keyboard language.',
                            sort_order=2)
        setup.indicators.append(keyboard_language)
        install_software = Indicator(
                            title=u'Install, uninstall a software application.',
                            description=u'Install, uninstall a software application',
                            sort_order=3)
        setup.indicators.append(install_software)    
        print_screen = Indicator(
                            title=u'Use keyboard print screen facility to capture a full screen, active window.',
                            description=u'Use keyboard print screen facility to capture a full screen, active window.',
                            sort_order=4)
        # Indicator Set Working with Icons
        icons = IndicatorSet(title=u'Work with Icons')
        icons.competence = operating_system
        common_icons = Indicator(
                            title=u'Identify common icons',
                            description=u'Identify common icons like those representing: files, folders, applications, printers, drives, recycle bin/wastebasket/trash.',
                            sort_order=0)
        icons.indicators.append(common_icons)
        select_move = Indicator(
                            title=u'Select and move icons.',
                            description=u'Select and move icons.',
                            sort_order=1)
        icons.indicators.append(select_move)
        create_icon = Indicator(
                            title=u'Create, remove a desktop shortcut icon, make an alias.',
                            description=u'Create, remove a desktop shortcut icon, make an alias.',
                            sort_order=2)
        icons.indicators.append(create_icon)
        use = Indicator(
                            title=u'Use an icon to open a file, folder, application.',
                            description=u'Use an icon to open a file, folder, application.',
                            sort_order=3)
        icons.indicators.append(use)                    
        # Indicator Set Using Window                
        using_windows = IndicatorSet(title=u'Using Windows')
        using_windows.competence = operating_system
        identify_parts = Indicator(
                            title=u'Identify the different parts of a window',
                            description=u'Identify the different parts of a window: title bar, menu bar, toolbar or ribbon,status bar, scroll bar.',
                            sort_order=0)
        using_windows.indicators.append(identify_parts)
        windows = Indicator(
                            title=u'Collapse, expand, restore, resize, move, close a window.',
                            description=u'Collapse, expand, restore, resize, move, close a window.',
                            sort_order=1)
        using_windows.indicators.append(windows)
        switch_windows = Indicator(
                            title=u'Switch between open windows.',
                            description=u'Switch between open windows.',
                            sort_order=2)
        using_windows.indicators.append(switch_windows)
        # Add competence file management  to the project
        file_management = Competence(title=u'File Management')
        file_management.meta_competence = technical
        file_management.description = u'Know about the main concepts of file management and be able to efficiently organize files and folders so that they are easy to identify and find.'
        using_managingfiles.competences.append(file_management)
        # Indicator set main concepts
        main_concepts = IndicatorSet(title=u'Main Concepts')
        main_concepts.competence = file_management
        organise_os = Indicator(
                            title=u'Understand how an operating system organizes drives, folders, files in a hierarchical structure.',
                            description=u'Understand how an operating system organizes drives, folders, files in a hierarchical structure.',
                            sort_order=0)
        main_concepts.indicators.append(organise_os)
        devices = Indicator(
                            title=u'Know devices used by an operating system to store files and folders',
                            description=u'Know devices used by an operating system to store files and folders like: hard disk, network drives, USB flash drive, CD-RW, DVD-RW',
                            sort_order=1)
        main_concepts.indicators.append(devices)
        file_measurements = Indicator(
                            title=u'Know how files, folders are measured',
                            description=u'Know how files, folders are measured: KB, MB, GB.',
                            sort_order=2)
        main_concepts.indicators.append(file_measurements)
        backing_up = Indicator(
                            title=u'Understand the purpose of regularly backing up data',
                            description=u'Understand the purpose of regularly backing up data to a removable storage device for off-site storage.',
                            sort_order=3)
        main_concepts.indicators.append(backing_up)
        online_filestorage = Indicator(
                            title=u'Understand the benefits of online file storage',
                            description=u'Understand the benefits of online file storage: convenient access, ability to share files.',
                            sort_order=4)
        main_concepts.indicators.append(online_filestorage)
        # Indicator set Files and Folders
        files_folders = IndicatorSet(title=u'Files and Folders')
        files_folders.competence = file_management
        open_window = Indicator(
                            title=u'Open a window to display folder name, size, location on a drive.',
                            description=u'Open a window to display folder name, size, location on a drive.',
                            sort_order=0)
        files_folders.indicators.append(open_window)
        expand_collapse = Indicator(
                            title=u'Expand, collapse views of drives, folders,',
                            description=u'Expand, collapse views of drives, folders.',
                            sort_order=1)
        files_folders.indicators.append(expand_collapse)
        navigate = Indicator(
                            title=u'Navigate to a folder, file on a drive,',
                            description=u'Navigate to a folder, file on a drive.',
                            sort_order=2)
        files_folders.indicators.append(navigate)
        create_folder = Indicator(
                            title=u'Create a folder and a further sub-folder.',
                            description=u'Create a folder and a further sub-folder.',
                            sort_order=3)
        files_folders.indicators.append(create_folder)
        # Indicator set Working with Files
        working_files = IndicatorSet(title=u'Working with Files')
        working_files.competence = file_management
        identify_files = Indicator(
                            title=u'Identify common file types',
                            description=u'Identify common file types: word processing files, spreadsheet files, database files, presentation files, portable document format files, image files, audio files, video files, compressed files, temporary files, executable files.',
                            sort_order=0)
        working_files.indicators.append(identify_files)
        text_application = Indicator(
                            title=u'Open a text editing application. Enter text into a file, name and save the file to a location on a drive.',
                            description=u'Open a text editing application. Enter text into a file, name and save the file to a location on a drive.',
                            sort_order=1)
        working_files.indicators.append(text_application)
        change_status = Indicator(
                            title=u'Change file status: read-only/locked, read-write.',
                            description=u'Change file status: read-only/locked, read-write.',
                            sort_order=2)
        working_files.indicators.append(change_status)
        sort_files = Indicator(
                            title=u'Sort files',
                            description=u'Sort files in ascending, descending order by name, size, type, date modified.',
                            sort_order=3)
        working_files.indicators.append(sort_files)
        good_practise = Indicator(
                            title=u'Recognize good practice in folder, file naming',
                            description=u'Recognize good practice in folder, file naming: use meaningful names for folders and files to help with recall and organization.', 
                            sort_order=4)
        working_files.indicators.append(good_practise)
        rename = Indicator(
                            title=u'Rename files, folders.',
                            description=u'Rename files, folders', 
                            sort_order=5)
        working_files.indicators.append(rename)
        # Indicator set Copy and Move
        copy_move = IndicatorSet(title=u'Copy and Move')
        copy_move.competence = file_management
        select = Indicator(
                            title=u'Select a file, folder individually or as a group of adjacent, non-adjacent files, folders.',
                            description=u'Select a file, folder individually or as a group of adjacent, non-adjacent files, folders.',
                            sort_order=0)
        copy_move.indicators.append(select)
        copy = Indicator(
                            title=u'Copy files, folders between folders and between drives.',
                            description=u'Copy files, folders between folders and between drives',
                            sort_order=1)
        copy_move.indicators.append(copy)
        move = Indicator(
                            title=u'Move files, folders between folders and between drives.',
                            description=u'Move files, folders between folders and between drives.',
                            sort_order=2)
        copy_move.indicators.append(move)
        # Indicator set Delete, Restore
        delete_restore = IndicatorSet(title=u'Delete, Restore')
        delete_restore.competence = file_management
        delete = Indicator(
                            title=u'Delete files, folders to the recycle bin/wastebasket/trash.',
                            description=u'Delete files, folders to the recycle bin/wastebasket/trash.',
                            sort_order=0)
        delete_restore.indicators.append(delete)
        restore = Indicator(
                            title=u'Restore files, folders from the recycle bin/wastebasket/trash.',
                            description=u'Restore files, folders from the recycle bin/wastebasket/trash.',
                            sort_order=1)
        delete_restore.indicators.append(restore)
        empty_bin = Indicator(
                            title=u'Empty the recycle bin/wastebasket/trash.',
                            description=u'Empty the recycle bin/wastebasket/trash.',
                            sort_order=2)
        delete_restore.indicators.append(empty_bin)
        # Indicator set Searching
        searching = IndicatorSet(title=u'Searching')
        searching.competence = file_management
        find_tool = Indicator(
                            title=u'Use the Find tool to locate a file, folder.',
                            description=u'Use the Find tool to locate a file, folder.',
                            sort_order=0)
        searching.indicators.append(find_tool)
        search_modeone = Indicator(
                            title=u'Search for files by all or part of file name, by content.',
                            description=u'Search for files by all or part of file name, by content.',
                            sort_order=1)
        searching.indicators.append(search_modeone)
        search_modetwo = Indicator(
                            title=u'Search for files by date modified, by date created, by size.',
                            description=u'Search for files by date modified, by date created, by size.',
                            sort_order=2)
        searching.indicators.append(search_modetwo)
        search_modethree = Indicator(
                            title=u'Search for files by using wildcards: file type, first letter of file name.',
                            description=u'Search for files by using wildcards: file type, first letter of file name',
                            sort_order=3)
        searching.indicators.append(search_modethree)
        view_list = Indicator(
                            title=u'View list of recently used files.',
                            description=u'View list of recently used files.',
                            sort_order=4)
        searching.indicators.append(view_list)
        # Add competence Utilities to the project
        utilities = Competence(title=u'Utilities')
        utilities.meta_competence = technical
        utilities.description = u'Use utility software to compress and extract large files and use anti-virus software to protect against computer viruses'
        using_managingfiles.competences.append(utilities)
        # Indicator set file compression
        file_compression = IndicatorSet(title=u'File Compression')
        file_compression.competence = utilities
        understand_filecompression = Indicator(
                            title=u'Understand what file compression means.',
                            description=u'Understand what file compression means.',
                            sort_order=0)
        file_compression.indicators.append(understand_filecompression)
        compress_file = Indicator(
                            title=u'Compress files in a folder on a drive',
                            description=u'Compress files in a folder on a drive',
                            sort_order=1)
        file_compression.indicators.append(compress_file)
        extract_file = Indicator(
                            title=u'Extract compressed files from a location on a drive.',
                            description=u'Extract compressed files from a location on a drive',
                            sort_order=2)
        file_compression.indicators.append(extract_file)
        # Indicator set anti-virus
        anti_virus = IndicatorSet(title=u'Anti-Virus')
        anti_virus.competence = utilities
        understand_virus = Indicator(
                            title=u'Understand what a virus is and the ways a virus can be transmitted onto a computer.',
                            description=u'Understand what a virus is and the ways a virus can be transmitted onto a computer.',
                            sort_order=0)
        anti_virus.indicators.append(understand_virus)
        use_software = Indicator(
                            title=u'Use anti-virus software to scan specific drives, folders, files.',
                            description=u'Use anti-virus software to scan specific drives, folders, files',
                            sort_order=1)
        anti_virus.indicators.append(use_software)
        update_software = Indicator(
                            title=u'Understand why anti-virus software needs to be updated regularly.',
                            description=u'Understand why anti-virus software needs to be updated regularly.',
                            sort_order=2)
        anti_virus.indicators.append(update_software)
        # Add competence printer management to the project
        printer_management = Competence(title=u'Printer Management')
        printer_management.meta_competence = technical
        printer_management.description = u'Demonstrate the ability to use simple text editing and print tools available within the operating system.'
        using_managingfiles.competences.append(printer_management)
        # Indicator set printer option
        printer_options = IndicatorSet(title=u'Printer Options')
        printer_options.competence = printer_management
        change_default_printer = Indicator(
                            title=u'Change the default printer from an installed printer list.',
                            description=u'Change the default printer from an installed printer list.',
                            sort_order=0)
        printer_options.indicators.append(change_default_printer)
        install_new_printer = Indicator(
                            title=u'Install a new printer on the computer.',
                            description=u'Install a new printer on the computer.',
                            sort_order=1)
        printer_options.indicators.append(install_new_printer)
        # Indicator set print
        printer = IndicatorSet(title=u'Print')
        printer.competence = printer_management
        print_document = Indicator(
                            title=u'Print a document from a text editing application',
                            description=u'Print a document from a text editing application.',
                            sort_order=0)
        printer.indicators.append(print_document)
        view_prints_progress = Indicator(
                            title=u'View a print job’s progress in a queue using a desktop print manager.',
                            description=u'View a print job’s progress in a queue using a desktop print manager.',
                            sort_order=1)
        printer.indicators.append(view_prints_progress)
        pause_restart_delete = Indicator(
                            title=u'Pause, re-start, delete a print job using a desktop print manager.',
                            description=u'Pause, re-start, delete a print job using a desktop print manager.',
                            sort_order=2)
        printer.indicators.append(pause_restart_delete)
        
        
        # Add two students
        anna = Student(first_name=u'Anna', last_name=u'Karenina', email=u"anna@seantis.ch", password=u'12345', interests=u'Russian food', experiences=u'cooking for grandma', hobbies='Dancing')
        scarlett = Student(first_name=u'Scarlett', last_name=u'O Hara', email=u"scarlett@seantis.ch", password=u'12345', hobbies='horse riding', interests=u'clothes and dramatic stylings', experiences=u'Has been desperate for a while')
        concepts_ict.students.append(anna)
        concepts_ict.students.append(scarlett)
        
        # Scarlett and Anna add journal entries
        entry_anna = JournalEntry()
        entry_anna.text = u'I learned how to regonize licensed software today. Really helpful knowledge!'
        entry_anna.user = anna
        entry_anna.date = datetime.datetime.now()
        entry_anna.project = concepts_ict
        entry_anna.indicators.append(licensed_software)
        
        entry_scarlett = JournalEntry()
        entry_scarlett.text = u'I know now what impacts on a computers performance. So I know what is important when buying a new one.'
        entry_scarlett.user = scarlett
        entry_scarlett.date = datetime.datetime.now()
        entry_scarlett.project = concepts_ict
        entry_scarlett.indicators.append(impact_performance)
        
        entry_scarlett_2 = JournalEntry()
        entry_scarlett_2.text = u'Bits and Bytes, I finally understand, it has got nothing to do with food... :)'
        entry_scarlett_2.user = scarlett
        entry_scarlett_2.date = datetime.datetime.now()
        entry_scarlett_2.project = concepts_ict
        entry_scarlett_2.indicators.append(storage_capacity)
        
        entry_anna_2 = JournalEntry()
        entry_anna_2.text = u'I moved my computer today and hey: no more pain! wow!'
        entry_anna_2.user = anna
        entry_anna_2.date = datetime.datetime.now()
        entry_anna_2.project = concepts_ict
        entry_anna_2.indicators.append(positioning)
        
        # Anna comments on Scarlett journal
        comment_anna = Comment()
        comment_anna.user = anna
        comment_anna.journal_entry = entry_scarlett_2
        comment_anna.date = datetime.datetime.now()
        comment_anna.text = u':D no, and WLAN ist no special kind of flan...'
        
        # Add two students
        buck = Student(first_name=u'Buck', last_name=u'Mulligan', email=u"buck@seantis.ch", password=u'12345', languages=u'English, German', interests=u'Mountains, Medicine, Time', experiences=u'None in working, but has been thinking as lot', hobbies='Being in the mountains, thinking about life and time' )
        hans = Student(first_name=u'Hans', last_name=u'Castrop', email=u"hans@seantis.ch", password=u'12345', languages=u'English, Gaelic', interests=u'Dinosaurs, Landscapes, Books', experiences=u'Worked in a newspaper magazine for a while', hobbies=u'Walking aorund Dublin, Drinking Guinness in a decent environment')
        using_managingfiles.students.append(buck)
        using_managingfiles.students.append(hans)
        
        # Add a teacher
        leopold = Teacher(first_name=u'Leopold', last_name=u'Bloom', email=u"leopold@seantis.ch", password=u'12345')
        concepts_ict.teachers.append(leopold)
        
        # Buck and Hans add journal entries
        entry_buck = JournalEntry()
        entry_buck.text = u'I learned how to change the desktop background today. Its my favourite footballteam now! Go Tigers!'
        entry_buck.user = buck
        entry_buck.date = datetime.datetime.now()
        entry_buck.project = using_managingfiles
        entry_buck.indicators.append(change_desktop_configuration)
        
        entry_hans = JournalEntry()
        entry_hans.text = u'I tried to print the recipe my grandma sent me. And it worked! Thanks, Omi.'
        entry_hans.user = hans
        entry_hans.date = datetime.datetime.now()
        entry_hans.project = using_managingfiles
        entry_hans.indicators.append(print_document)
        
        entry_hans_2 = JournalEntry()
        entry_hans_2.text = u'Heurekà! I finally know the difference between CD-RW and DVD-RW.'
        entry_hans_2.user = hans
        entry_hans_2.date = datetime.datetime.now()
        entry_hans_2.project = using_managingfiles
        entry_hans_2.indicators.append(devices)
        
        entry_buck_2 = JournalEntry()
        entry_buck_2.text = u'Today, I showed Hans how he can set his mother tongue as default keyboarde language. He can now type these funny Umlauts'
        entry_buck_2.user = buck
        entry_buck_2.date = datetime.datetime.now()
        entry_buck_2.project = using_managingfiles
        entry_buck_2.indicators.append(keyboard_language)
        
        # Hans comments on Buck journal
        comment_hans = Comment()
        comment_hans.user = hans
        comment_hans.journal_entry = entry_buck_2
        comment_hans.date = datetime.datetime.now()
        comment_hans.text = u'"These funny Umlauts" are important! Thank you for your help, maybe I can teach you in return how to use a keyboard in a decent way without breaking it... :)'