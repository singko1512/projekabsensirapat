<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        // 1. Tabel Admin
        Schema::create('admins', function (Blueprint $table) {
            $table->id('id_Admin');
            $table->string('username')->unique();
            $table->string('nama');
            $table->string('password');
            $table->timestamps();
        });

        // 2. Tabel Agenda Rapat
        Schema::create('agendas', function (Blueprint $table) {
            $table->id('id_agenda');
            $table->string('nama_agenda'); // Sesuai kolom request kita sebelumnya
            $table->date('tanggal');
            $table->time('waktu');
            $table->string('lokasi');
            $table->string('status_qr')->default('nonaktif'); // Pengganti boolean biar gampang ditrigger
            $table->timestamps();
        });

        // 3. Tabel Kunjungan
        Schema::create('kunjungans', function (Blueprint $table) {
            $table->id('id_Kunjungan');
            $table->string('keperluan');
            $table->date('tanggal_kunjungan');
            $table->timestamps();
        });

        // 4. Tabel Data Aduan
        Schema::create('aduans', function (Blueprint $table) {
            $table->id('id_aduan');
            $table->string('nama_pengadu');
            $table->text('isi_aduan');
            $table->string('status')->default('pending');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('aduans');
        Schema::dropIfExists('kunjungans');
        Schema::dropIfExists('agendas');
        Schema::dropIfExists('admins');
    }
};
