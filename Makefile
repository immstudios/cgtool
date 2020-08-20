.PHONY: install

SYSDIR = /etc/systemd/system
APPDIR = /opt/cgtool
UNITS = $(SYSDIR)/cgtool.service
UNITSSRC = $(APPDIR)/support/cgtool.service

install : $(UNITS)

$(UNITS): $(UNITSSRC)
	cp $(APPDIR)/support/cgtool.service $(SYSDIR)/cgtool.service
